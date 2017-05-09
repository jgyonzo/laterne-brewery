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
		$stmt = $mysqli->prepare("SELECT temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp11, temp12, temp1_cfg, temp2_cfg, temp3_cfg, temp4_cfg, temp5_cfg, temp6_cfg, temp7_cfg, temp8_cfg, temp9_cfg, temp10_cfg, temp11_cfg, temp12_cfg, output1, output2, output3, output4, output5, output6, output7, output8, output9, output10, output11, output12 FROM temps4 ORDER BY created_at DESC LIMIT 1");
		$stmt->execute();
		$stmt->bind_result($res['temp1'], $res['temp2'], $res['temp3'], $res['temp4'], $res['temp5'], $res['temp6'], $res['temp7'], $res['temp8'], $res['temp9'], $res['temp10'], $res['temp11'], $res['temp12'], $res['temp1_cfg'], $res['temp2_cfg'], $res['temp3_cfg'], $res['temp4_cfg'], $res['temp5_cfg'], $res['temp6_cfg'], $res['temp7_cfg'], $res['temp8_cfg'], $res['temp9_cfg'], $res['temp10_cfg'], $res['temp11_cfg'], $res['temp12_cfg'], $res['output1'], $res['output2'], $res['output3'], $res['output4'], $res['output5'], $res['output6'], $res['output7'], $res['output8'], $res['output9'], $res['output10'], $res['output11'], $res['output12']);
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
				<div class="label">BAN FRIO [<?php print $lastTemps['temp6_cfg']; ?> &deg;] <?php if($lastTemps['output6'] == 0) print "[on]"; ?></div><div class="label">CAM FRIO [<?php print $lastTemps['temp7_cfg']; ?> &deg;] <?php if($lastTemps['output7'] == 0) print "[on]"; ?></div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp6'], 0); ?><span>.<?php  print tempParts($lastTemps['temp6'], 1); ?></span><strong>&deg;</strong>
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
							<?php print tempParts($lastTemps['temp7'], 0); ?><span>.<?php  print tempParts($lastTemps['temp7'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="label">FV3 [<?php print $lastTemps['temp5_cfg']; ?> &deg;] <?php if($lastTemps['output5'] == 0) print "[on]"; ?></div><div class="label">FV1 [<?php print $lastTemps['temp1_cfg']; ?> &deg;] <?php if($lastTemps['output1'] == 0) print "[on]"; ?></div>
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
							<?php print tempParts($lastTemps['temp1'], 0); ?><span>.<?php print tempParts($lastTemps['temp1'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="label">FV4 [<?php print $lastTemps['temp8_cfg']; ?> &deg;] <?php if($lastTemps['output8'] == 0) print "[on]"; ?></div><div class="label">FV2 [<?php print $lastTemps['temp2_cfg']; ?> &deg;] <?php if($lastTemps['output2'] == 0) print "[on]"; ?></div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp8'], 0); ?><span>.<?php  print tempParts($lastTemps['temp8'], 1); ?></span><strong>&deg;</strong>
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
							<?php print tempParts($lastTemps['temp2'], 0); ?><span>.<?php  print tempParts($lastTemps['temp2'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="label">FV5 [<?php print $lastTemps['temp9_cfg']; ?> &deg;] <?php if($lastTemps['output9'] == 0) print "[on]"; ?></div><div class="label">BBT1 [<?php print $lastTemps['temp3_cfg']; ?> &deg;] <?php if($lastTemps['output3'] == 0) print "[on]"; ?></div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp9'], 0); ?><span>.<?php  print tempParts($lastTemps['temp9'], 1); ?></span><strong>&deg;</strong>
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
							<?php print tempParts($lastTemps['temp3'], 0); ?><span>.<?php  print tempParts($lastTemps['temp3'], 1); ?></span><strong>&deg;</strong>
						  </div>
						</div>
					  </div>
					</div>
				</div>
				<div class="label">FV6 [<?php print $lastTemps['temp10_cfg']; ?> &deg;] <?php if($lastTemps['output10'] == 0) print "[on]"; ?></div><div class="label">BBT2 [<?php print $lastTemps['temp4_cfg']; ?> &deg;] <?php if($lastTemps['output4'] == 0) print "[on]"; ?></div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp10'], 0); ?><span>.<?php  print tempParts($lastTemps['temp10'], 1); ?></span><strong>&deg;</strong>
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
				<div class="label">AMBIENT</div><div class="label">N/A</div>
				<div class="de">
					<div class="den">
					  <div class="dene">
						<div class="denem">
						  <div class="deneme">
							<?php print tempParts($lastTemps['temp11'], 0); ?><span>.<?php  print tempParts($lastTemps['temp11'], 1); ?></span><strong>&deg;</strong>
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
