/* 

Module to control reading from SDRAM 

Last Modified: 25 Jan 2018

Hannah Fogel

*/

module sdram_read( 
	// External Pins
	input clk,
	input reset_n,
	input start_read,
	
	// SDRAM interface
	input read_control_done,
	input read_control_early_done,
	input [31:0] user_read_buffer_data,
	input user_read_data_available,
	output read_control_fixed_location,
	output [31:0] control_read_base,
	output [31:0] control_read_length,
	output reg read_control_go,
	output reg user_read_ack,
	
	
	// SPI interface
	output reg [31:0] data_to_spi
);
	
	
// define parameters 
// num_bytes to read will be sent from RPi

reg [31:0] start_address = 32'h0;					// base address to read from 
wire [31:0] num_bytes = 32'h00000040;						// number of bytes to read - should be a multiple of 4 for 32-bit data

assign read_control_fixed_location = 1;			// master address unchanging	
assign control_read_base = start_address;			
assign control_read_length = num_bytes;	

reg [1:0] state = 2'b00;
reg [31:0] data_in;

always @ (posedge clk or negedge reset_n)
	begin
	if (reset_n == 0)
		begin
			read_control_go <= 0;
			user_read_ack <= 0;
			state <= 2'b00;
		end //if
	else begin
		case (state)
			2'b00: begin						
				if (start_read == 0) begin
					state <= 2'b00;
					user_read_ack <= 0;
					read_control_go <= 0;
				end else begin
					user_read_ack <= 0;
					read_control_go <= 1;
					state <= 2'b01;
				end
			end // state 0
			
			2'b01: begin
				read_control_go <= 0;
				user_read_ack <= 0;
				if (user_read_data_available == 1) begin	
					state <= 2'b10;
				end else begin
					state <= 2'b01;
				end
			end // state 1
			
			2'b10: begin
				data_in <= user_read_buffer_data;		// register incoming data (n bits wide)
				state <= 2'b11;
			end // state 2
			
			2'b11: begin
				data_to_spi <= data_in;
				user_read_ack <= 1;
				if (read_control_done == 1) begin
					start_address <= (start_address + num_bytes);
					state <= 2'b00;
				end else begin
					state <= 2'b01;
				end
			end // state 3
		
		endcase
	
	end //else

end // always		
		
		
endmodule 
