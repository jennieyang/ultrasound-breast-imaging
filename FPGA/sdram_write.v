/* 

Module to control capturing data from ADS5263 ADC and writing it to SDRAM 


Last Modified: 9 Mar 2018

Hannah Fogel

*/

module sdram_write (
		// External Pins
		input  clk,
		input  reset_n,
		input stop_write,			// so not trying to read and write at the same time
		//input [7:0] num_bytes,		// from SPI module
		//input [31:0] data_out,
		output [2:0] LEDG,
		
		// SDRAM interface
		input  write_buffer_full,
		input  write_control_done,
		output wire write_control_fixed_location,
		output wire [31:0] control_write_base,
		output wire [31:0] control_write_length,
		output reg write_control_go,
		output reg user_data_valid,
		output reg [31:0] user_write_buffer_data,
		
		// SPI Interface
		input [31:0] from_spi,		// will contain number of bytes to store
		
		// ADC Interface
		
		input lvds_dclk_p, 			// DDR bit clock from ADS5263, freq=4*fs
		input lvds_fclk_p,			// frame clock from ADS5263, freq = 0.5*fs
		
		// data received from ADS5263 - 2 wire interface, one port for each byte-wise wire
		input [1:0] lvds_ch1_p
		//input [1:0] lvds_ch2_p,
		//input [1:0] lvds_ch3_p,
		//input [1:0] lvds_ch4_p
	//	output reg [31:0] data_to_ram					// to see in SignalTap
		
		
		);		

// Set status LED functions	
assign LEDG[0] = reset_n;
assign LEDG[1] = adc_data_ready;
assign LEDG[2] = ~pll_locked;
		
		
// Instantiate ALTLVDS_RX megafunction
// 2-wire, 8x de-serialization, 1 ADC input channel 
// fs = 40 MHz, dclk =  160 MHz, fclk = 20 MHz
// ** change SDC file if changing fs **
// Internal PLL - source synchronous, 90 deg phase shift (center-aligned data) CHANGED to 180 as per IP Core UG
wire pll_locked;
wire [23:0] rx_data_out; //wire [31:0] rx_data_out;
wire rx_clk_out;
reg data_align_pulse;
reg adc_data_ready;

altlvds_in	altlvds_in_inst (
	.rx_data_align ( data_align_pulse ),
	.rx_in ( {lvds_ch1_p[1], lvds_ch1_p[0], lvds_fclk_p} ),
	.rx_inclock ( lvds_dclk_p ),
	.rx_locked ( pll_locked ),
	.rx_out ( rx_data_out ),
	.rx_outclock ( rx_clk_out )
	);	

	
	// format received data into 16-bit word per channel
// first channel in => MSB of data out - confirmed in IP Core User Guide 9 Feb 2018
// ==> frame is last in list of inputs, therefore is bits 15..0 of rx_out		
		
		
// State Machine for 1 channel, 2-wire, 8xSERDES mode
reg [1:0] st = 2'b0;
reg [15:0] ch1data1;
reg [31:0] data_to_ram; //change to output to see in SignalTap

always @ (posedge rx_clk_out) begin
	case(st)
		2'b00: begin
			if (rx_data_out[7:0] == 8'hFF) begin 
				data_align_pulse <=0;
				adc_data_ready <= 0;
				st <= 2'b01; 
			end else begin
				data_align_pulse <= 1;
				adc_data_ready <= 0;
				st <= 2'b11;
			end // else
		end // state 0
		
		2'b01: begin 
			ch1data1 = rx_data_out[23:8]; // store {wire2, wire1}
			data_align_pulse <=0;
			adc_data_ready <=1;
			st <= 2'b10;
		end 
		
		2'b10: begin
			data_to_ram = {ch1data1,rx_data_out[23:8]};	// two consecutive 16-bit samples
			data_align_pulse <=0;
			adc_data_ready <=1;
			st <= 2'b01;
		end // state 1
		
		2'b11: begin
			data_align_pulse <= 0;
			adc_data_ready <= 0;
			st <= 2'b00;
		end // state 2
		
	endcase
end //always		
		
//////////////////////////////////////////////////////////////////////////////////////////////////////
// SDRAM WRITE

wire [31:0] num_bytes = 32'h00000040; 			// from SPI module: number of bytes to store in RAM - should be a multiple of 4 (<255) for 32-bit data
reg [1:0] state;
reg [31:0] base_address = 32'h00000000;

// define constants
assign write_control_fixed_location = 1; 		// master address unchanging
assign control_write_base = base_address ;		// must be a mulitple of 4 for 32-bit data		
assign control_write_length = num_bytes; 		// must be a mulitple of 4 for 32-bit data

// for debugging
reg full;
reg done =0;
//reg [3:0] leds; 

//  indicator LEDs
//assign LEDG[7:4] = leds;
//assign LEDG[0] = full;
//assign LEDG[1] = done;

reg [31:0] dout;

always @ (posedge clk or negedge reset_n)
	begin
	if (reset_n == 0)
		begin
			state <= 2'b00;
			full <= 0;
			done <= 0;
			user_data_valid <= 0;	
			write_control_go <= 0;
			base_address <= 32'b0;
		end
	else begin
			case (state) 		
				2'b00: begin 			 				// State 0: initiate write
					if (stop_write == 1) begin
						user_data_valid <= 0;	
						write_control_go <= 0;
						state <= 2'b00;
					end else begin
						done <= 0; 
						user_data_valid <= 0;	
						write_control_go <= 1;
						state <= 2'b01;
					end
				end // state 0
				
				2'b01:	begin							// State 1: Load data and check if buffer is full	
					write_control_go <= 0;
					user_data_valid <= 0;
					user_write_buffer_data <= data_to_ram;
					if (write_buffer_full == 0) begin
						full <= 0;
						state <= 2'b10;
					end // if
					else begin 
						full <= 1;
						state <= 2'b01;
					end // else
				end 	// state 1

				2'b10: begin			 				// State 2: Assert data is valid and check if transaction is done
					write_control_go <= 0;
					user_data_valid <= 1;
					if (write_control_done == 0) begin
						done <= 0;
						state <= 2'b01;
					end // if
					else begin 
						base_address <= (base_address + num_bytes);
						done <= 1;
						state <= 2'b00;
					end // else
				end // state 2

			endcase
 		end // else
	end // always 

endmodule
				
			
	
