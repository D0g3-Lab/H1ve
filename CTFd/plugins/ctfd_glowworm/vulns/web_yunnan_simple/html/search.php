<?php
	include 'header.php';
	include_once('config.php');
	if (!empty($_GET['id'])) {
	$id=$_GET['id'];
	$query = "SELECT * FROM news WHERE id=$id";
	$data = mysqli_query($dbc,$query);	
	}
	$com = mysqli_fetch_array($data); 
?>
<!-- banner -->
	<div class="banner1">
	</div>
<!-- //banner -->
<!-- about -->
	<div class="about">
		<div class="container">
			<ol class="breadcrumb breadco">
			  <li><a href="./index.php">主页</a></li>
			  <li class="active">搜索</li>
			</ol>
			<center>
			<div class="about-grids">
				<div class="col-md-6 about-grid">
					<h3>搜索结果</h3>
					<div class="about-gd">
					
						<?php
							var_dump($com);					
						?>
							
					</div>
				</div>
			</div>
		</div>
	</div>
<!-- //about -->
<?php
	include 'footer.php';
?>
