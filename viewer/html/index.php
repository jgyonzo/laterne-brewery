<?php
	// Make sure you set the database connection on the next line:
	$mysqli = new mysqli("127.0.0.1", "root", "raspberry", "Temperaturas");

	/* check connection */
	if ($mysqli->connect_errno) {
		header("HTTP/1.0 500 Internal Server Error");
		exit();
	}

	$lastTemps = getLastTemps($mysqli);
	
	$mysqli->close();

	if($_GET['format'] == json) {
		header('Content-Type: application/json');
		print json_encode($lastTemps);
		exit;
	}
	
	header('Refresh: 10; url=index.php');

	function getLastTemps($mysqli) {
		$stmt = $mysqli->prepare("SELECT temp1, temp2, temp3, temp4, temp5, created_at FROM temps4 ORDER BY created_at DESC LIMIT 1");
		$stmt->execute();
		$stmt->bind_result($res['temp1'], $res['temp2'], $res['temp3'], $res['temp4'], $res['temp5'], $res['created_at']);
		$stmt->fetch();
		return $res;
	}
	
	function tempParts($temp, $index) {
		$parts = explode('.', number_format($temp, 1));
		return $parts[$index];
	}

?>
<html>
	<head>
		<title>Temperatures</title>
		<link rel="stylesheet" type="text/css" href="./css/style.css" />
		<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
	</head>
	<body>
		<div class="content">
			<div class="thermometers">
				<div class="label">FV1</div><div class="label">FV2</div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp1'], 0); ?><span>.<?php  print tempParts($lastTemps['temp1'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp2'], 0); ?><span>.<?php print tempParts($lastTemps['temp2'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="label">BBT1</div><div class="label">BBT2</div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp3'], 0); ?><span>.<?php  print tempParts($lastTemps['temp3'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp4'], 0); ?><span>.<?php  print tempParts($lastTemps['temp4'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="label">FV3</div><div class="label">N/A</div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp5'], 0); ?><span>.<?php  print tempParts($lastTemps['temp5'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							0<span>.0</span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
			</div>
			
		</div>
	</body>
</html>
