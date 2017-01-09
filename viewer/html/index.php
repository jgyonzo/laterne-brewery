<?php
	// Make sure you set the database connection on the next line:
	$mysqli = new mysqli("127.0.0.1", "root", "raspberry", "Temperaturas");

	/* check connection */
	if ($mysqli->connect_errno) {
		header("HTTP/1.0 500 Internal Server Error");
		exit();
	}

	$lastTemps = getLastTemps($mysqli);
	$coldTemps = getColdTemps($mysqli);
	
	$mysqli->close();

	if($_GET['format'] == json) {
		header('Content-Type: application/json');
		print json_encode($lastTemps);
		exit;
	}
	
	header('Refresh: 10; url=index.php');

	function getLastTemps($mysqli) {
		$stmt = $mysqli->prepare("SELECT temp1, temp2, temp3, temp4, temp5, temp1_cfg, temp2_cfg, temp3_cfg, temp4_cfg, temp5_cfg, output1, output2, output3, output4, output5 FROM temps4 ORDER BY created_at DESC LIMIT 1");
		$stmt->execute();
		$stmt->bind_result($res['temp1'], $res['temp2'], $res['temp3'], $res['temp4'], $res['temp5'], $res['temp1_cfg'], $res['temp2_cfg'], $res['temp3_cfg'], $res['temp4_cfg'], $res['temp5_cfg'], $res['output1'], $res['output2'], $res['output3'], $res['output4'], $res['output5']);
		$stmt->fetch();
		return $res;
	}
	
	function getColdTemps($mysqli) {
		$stmt = $mysqli->prepare("SELECT  temp_cold_room , temp_chiller , temp_cold_room_cfg , temp_chiller_cfg , output_chiller , output_cold_room , timer_off_chiller , timer_off_cold_room FROM temps_cold");
		$stmt->execute();
		$stmt->bind_result($res['temp_cold_room'], $res['temp_chiller'], $res['temp_cold_room_cfg'], $res['temp_chiller_cfg'], $res['output_chiller'], $res['output_cold_room'], $res['timer_off_chiller'], $res['timer_off_cold_room']);
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
		<title>Laterne Brewery & Co. - Control de temperaturas</title>
		<link rel="stylesheet" type="text/css" href="./css/style.css" />
		<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
	</head>
	<body>
		<div class="content">
			<div class="thermometers">
				<div class="label">FV1 [<?php print $lastTemps['temp1_cfg']; ?> &deg;] <?php if($lastTemps['output1'] == 0) print "[on]"; ?></div><div class="label">FV2 [<?php print $lastTemps['temp2_cfg']; ?> &deg;] <?php if($lastTemps['output2'] == 0) print "[on]"; ?></div>
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
				<div class="label">BBT1 [<?php print $lastTemps['temp3_cfg']; ?> &deg;] <?php if($lastTemps['output3'] == 0) print "[on]"; ?></div><div class="label">BBT2 [<?php print $lastTemps['temp4_cfg']; ?> &deg;] <?php if($lastTemps['output4'] == 0) print "[on]"; ?></div>
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
				<div class="label">FV3 [<?php print $lastTemps['temp5_cfg']; ?> &deg;] <?php if($lastTemps['output5'] == 0) print "[on]"; ?></div><div class="label">N/A</div>
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


				<div class="label">Banco [<?php print $coldTemps['temp_chiller']; ?> &deg;] <?php if($coldTemps['output_chiller'] == 0) print "[on]"; ?><?php if($coldTemps['timer_off_chiller'] == 1) print "[d]"; ?> </div> <div class="label">Cámara [<?php print $coldTemps['temp_cold_room']; ?> &deg;] <?php if($coldTemps['output_cold_room'] == 0) print "[on]"; ?><?php if($coldTemps['timer_off_cold_room'] == 1) print "[d]"; ?></div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($coldTemps['temp_chiller'], 0); ?><span>.<?php  print tempParts($coldTemps['temp_chiller'], 1); ?></span><strong>&deg;</strong>
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
							<?php print tempParts($coldTemps['temp_cold_room'], 0); ?><span>.<?php print tempParts($coldTemps['temp_cold_room'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
			</div>
			
		</div>
	</body>
</html>
