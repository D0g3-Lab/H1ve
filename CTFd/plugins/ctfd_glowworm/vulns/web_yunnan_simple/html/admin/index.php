<?php 
include_once('../config.php');
if (isset($_SESSION['username'])) {
	include_once('header.php');

?>
<!-- banner -->
	<div class="banner1">
	</div>
<!-- //banner -->
<!-- single -->
	<div class="single">
		<div class="container">
			<div class="single-page-artical">
				<div class="artical-content">
					<h3>flag:<?php system("cat /flag")?></h3>
					<img class="img-responsive" src="../images/banner.jpg" alt=" " />
					<p></p>
				</div>
				<div class="artical-links">
					<ul>
						<li><span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>September 15,2015</li>
						<li><a href="#"><span class="glyphicon glyphicon-user" aria-hidden="true"></span>admin</a></li>
						<li><a href="#"><span class="glyphicon glyphicon-envelope" aria-hidden="true"></span>No comments</a></li>
						<li><a href="#"><span class="glyphicon glyphicon-bookmark" aria-hidden="true"></span>View posts</a></li>
						<li><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>permalink</li>
					</ul>
				</div>
				<div class="comment-grid-top">
					<h3>回复</h3>
					<div class="comments-top-top">
						<div class="top-comment-left">
							<a href="#"><img class="img-responsive" src="images/co.png" alt=""></a>
						</div>
						<div class="top-comment-right">
							<ul>
								<li><span class="left-at"><a href="#">Admin</a></span></li>
								<li><span class="right-at">September 15, 2015 at 10.30am</span></li>
								<li><a class="reply" href="#">Reply</a></li>
							</ul>
						<p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout.The point of using Lorem Ipsum is that it has a more-or-less </p>
						</div>
						<div class="clearfix"> </div>
					</div>
					<div class="comments-top-top top-grid-comment">
						<div class="top-comment-left">
							<a href="#"><img class="img-responsive" src="images/co.png" alt=""></a>
						</div>
						<div class="top-comment-right">
							<ul>
								<li><span class="left-at"><a href="#">Admin</a></li>
								<li><span class="right-at">September 15, 2015 at 10.30am</span></li>
								<li><a class="reply" href="#">Reply</a></li>
							</ul>
						<p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout.The point of using Lorem Ipsum is that it has a more-or-less </p>
						</div>
						<div class="clearfix"> </div>
					</div>
				</div>			
				<div class="artical-commentbox">
					<h3>上传文件</h3>
					<div class="table-form">
						<form action="upload.php" method="post" enctype="multipart/form-data" name="upload">
							<input type="file" name="pic" value="Name" >
							<hr/>
							
							<input type="submit" value="上传">
						</form>
					</div>
				</div>	
			</div>
		</div>
	</div>
<!-- single -->
<?php 
	require_once('footer.php');
}
else {
	not_find($_SERVER['PHP_SELF']);
}

?>
