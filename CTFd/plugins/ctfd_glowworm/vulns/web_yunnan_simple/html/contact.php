<?php
	include 'header.php';
	$file_path = $_GET['path'];
	if(file_exists($file_path)){
	$fp = fopen($file_path,"r");
	$str = fread($fp,filesize($file_path));
	echo $str = str_replace("\r\n","<br />",$str);
							}
	
?>
<!-- banner -->
	<div class="banner1">
	</div>
<!-- //banner -->
<!-- contact -->
	<div class="contact">
		
		<div class="contact-grids">
			<div class="container">
			<ol class="breadcrumb breadco">
				<li><a href="#">Home</a></li>
				<li class="active">Contact Us</li>
			</ol>
			<div class="col-md-3 contact-grid">
				<div class="call">
					<div class="col-xs-3 contact-grdl">
						<span class="glyphicon glyphicon-phone" aria-hidden="true"></span>
					</div>
					<div class="col-xs-9 contact-grdr">
						<ul>
							<li>+3402 890 679</li>
							<li>+5356 890 679</li>
						</ul>
					</div>
					<div class="clearfix"> </div>
				</div>
				<div class="address">
					<div class="col-xs-3 contact-grdl">
						<span class="glyphicon glyphicon-send" aria-hidden="true"></span>
					</div>
					<div class="col-xs-9 contact-grdr">
						<ul>
							<li>345 Diamond Street,</li>
							<li>Greece.</li>
						</ul>
					</div>
					<div class="clearfix"> </div>
				</div>
				<div class="mail">
					<div class="col-xs-3 contact-grdl">
						<span class="glyphicon glyphicon-envelope" aria-hidden="true"></span>
					</div>
					<div class="col-xs-9 contact-grdr">
						<ul>
							<li><a href="mailto:info@example.com">info@example.com</a></li>
						</ul>
					</div>
					<div class="clearfix"> </div>
				</div>
			</div>
			<div class="col-md-5 contact-grid">
				<form>
					<input type="text" value="Name" onfocus="this.value = '';" onblur="if (this.value == '') {this.value = 'Name';}" required="">
					<input type="text" value="Email" onfocus="this.value = '';" onblur="if (this.value == '') {this.value = 'Email';}" required="">
					<textarea type="text"  onfocus="this.value = '';" onblur="if (this.value == '') {this.value = 'Message...';}" required="">Message...</textarea>
					<input type="submit" value="Send" >
				</form>
			</div>
			<div class="col-md-4 contact-grid">
				<div class="newsletter">
					<h3><span class="glyphicon glyphicon-envelope" aria-hidden="true"></span>Newsletter</h3>
				</div>
				<form>
					<input type="text" value="Email" onfocus="this.value = '';" onblur="if (this.value == '') {this.value = 'Email';}" required="">
					<input type="submit" value="Subscribe" >
				</form>
			</div>
			<div class="clearfix"> </div>
			</div>
		</div>
	</div>
<!-- contact -->
<?php
	include 'footer.php';
?>
