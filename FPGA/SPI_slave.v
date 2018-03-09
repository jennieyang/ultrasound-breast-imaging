/* SPI Slave Module

to communicate with RPi

SPI Mode 3 - 
	Change data (sdout) @ NEGEDGE SCK,
	Read data (sdin) @ posedge SCK

Based on example from http://opencores.com/project,spi_verilog_master_slave

Changes: 

8 Feb 2018
	- Integrated proj w/ altlvds_rx
	- 'to_sdram' will now contain info such as number of bytes to store 

TO DO (as of Feb 6): check why zeros are sent to sdram module

Hannah Fogel

*/

module SPI_slave (rstb,ss,sck,sdin,sdout,done,to_sdram,from_sdram, sclk_out, miso_out, ssel_out);
  // SPI wires
  input rstb,ss,sck,sdin;
  output sdout;          			 			// MISO
  
  // connected to sdram_write module
  //output reg start_ram_tx;						// for testing; will come directly from RPi as "trigger," then pulled low after x amount of time
  output reg [31:0] to_sdram;
  
  
  // connected to sdram_read module 
  input [31:0] from_sdram;
  
  // Indicator LED
  output reg done;
  
  // To see SPI signals on Logic Analyzer
  output sclk_out, miso_out, ssel_out;
  
  assign sclk_out = sck;
  assign miso_out = sdout;
  assign ssel_out = ss;  

  reg [31:0] treg;
  reg [31:0] rreg;
  reg [7:0] nb;
  wire sout;
  wire mlb;
  wire tri_en;
  
  assign mlb =1 ; // MSB first
  assign tri_en = 1;	// no tristate output
  assign sout=mlb?treg[31]:treg[0];
  assign sdout=( (!ss)&&tri_en )?sout:1'bz; //if 1=> send data  else TRI-STATE sdout
 
////read from  sdin
always @(posedge sck or negedge rstb)
  begin
	 if (rstb==0)
		begin rreg = 32'h00;  to_sdram = 32'h00; done = 0; nb = 0; end //start_ram_tx =0; end   //
	else begin
		if (!ss) begin 
			if(mlb==0)  //LSB first, in@msb -> right shift
				begin rreg ={sdin,rreg[31:1]}; end
			else     //MSB first, in@lsb -> left shift
				begin rreg ={rreg[30:0],sdin}; end  
		//increment bit count
			nb=nb+8'b1;
			if(nb!=8'h20) begin			// count up to 32 bits
				done=0;
				//start_ram_tx = 0;
			end 
			else begin 						// when bit count reaches 32
				to_sdram=rreg; 			// send received bits to sdram_write module
				done=1; 
				//start_ram_tx = 1;			 
				nb=0;  
			end 	// else
		end	 //if(!ss)
	end //else
  end // always
 
//send to  sdout
always @(negedge sck or negedge rstb)
  begin
	if (rstb==0)
		begin treg = 32'h00000000; end
	else begin
		if(!ss) begin			
			if(nb==0) treg=from_sdram;
			else begin
			   if(mlb==0)  //LSB first, out=lsb -> right shift
					begin treg = {1'b1,treg[31:1]}; end
			   else     //MSB first, out=msb -> left shift
					begin treg = {treg[30:0],1'b1}; end			
			end
		end //!ss
	 end //rstb	
  end //always

endmodule
