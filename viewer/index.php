<?php
	// Make sure you set the database connection on the next line:
	$mysqli = new mysqli("127.0.0.1", "root", "raspberry", "Temperaturas");

	/* check connection */
	if ($mysqli->connect_errno) {
		header("HTTP/1.0 500 Internal Server Error");
		exit();
	}

	$lastTemps = getLastTemps($mysqli);
	$lastAVGTemps = getAVGTemps($mysqli);
	$last24hourValues = last24hourValues($mysqli);
	
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
	
	function getAVGTemps($mysqli) {
		$stmt = $mysqli->prepare("SELECT AVG(temp1), AVG(temp2) FROM temps3 WHERE created_at >= SYSDATE() - INTERVAL 1 DAY");
		$stmt->execute();
		$stmt->bind_result($res['temp1'], $res['temp2']);
		$stmt->fetch();
		return $res;
	}

	function last24hourValues($mysqli) {
		$stmt = $mysqli->prepare("SELECT temp1, temp2, created_at FROM temps WHERE created_at >= SYSDATE() - INTERVAL 1 DAY");
		$stmt->execute();
		$stmt->bind_result($res['temp1'], $res['temp2'], $res['created_at']);
		$rows = array();

		$i = 0;
		while($stmt->fetch()) {
			$rows[$i] = array();
            foreach($res as $k=>$v)
                $rows[$i][$k] = $v;
            $i++;
		}
		return $rows;
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
		<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
		<script src="./amcharts/amcharts.js" type="text/javascript"></script> 
		<script type="text/javascript" src="./js/common.js"></script>
		<script type="text/javascript">
			
			var lineChartData = [
			<?php foreach($last24hourValues as $row) { ?>
			{
                date: calcTime(<?php print strtotime($row['created_at']) * 1000; ?>, 2),
                temp1: <?php print number_format($row['temp1'], 2); ?>,
                temp2: <?php print number_format($row['temp2'], 2); ?>
            },
			<?php } ?>
			];
			
			function calcTime(unixTime, offset) {

				// create Date object for current location
				d = new Date(unixTime);

				// convert to msec
				// add local time zone offset
				// get UTC time in msec
				utc = d.getTime() + (d.getTimezoneOffset() * 60000);

				// create new Date object for different city
				// using supplied offset
				nd = new Date(utc + (3600000*offset));
				return nd;

			}
			
			function formatLabel(value, valueString, axis){
				// let's say we dont' want minus sign next to negative numbers
				if(value < 0)
				{
					valueString = valueString.substr(1);
				}
				
				// and we also want a letter C to be added next to all labels (you can do it with unit, but anyway)
				valueString = valueString + "° C";
				return valueString;
			}
		
			AmCharts.ready(function () {
                var chart = new AmCharts.AmSerialChart();
                chart.dataProvider = lineChartData;
                chart.pathToImages = "../amcharts/images/";
                chart.categoryField = "date";
				chart.balloon.bulletSize = 5;

                // sometimes we need to set margins manually
                // autoMargins should be set to false in order chart to use custom margin values
                chart.marginLeft = 0;
                chart.marginBottom = 0;
                chart.marginTop = 0;

                // AXES
                // category                
                var categoryAxis = chart.categoryAxis;
                categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
                categoryAxis.minPeriod = "ss"; // our data is daily, so we set minPeriod to DD
                categoryAxis.inside = true;
                categoryAxis.gridAlpha = 0;
                categoryAxis.tickLength = 0;
                categoryAxis.axisAlpha = 0;

                // value
                var valueAxis = new AmCharts.ValueAxis();
				valueAxis.dashLength = 1;
                valueAxis.axisAlpha = 0;
				//set label function which will format values
				valueAxis.labelFunction = formatLabel;
				
                chart.addValueAxis(valueAxis);

                // GRAPH
                var graph = new AmCharts.AmGraph();
                graph.type = "line";
                graph.valueField = "temp1";
                graph.lineColor = "#5fb503";
                graph.negativeLineColor = "#efcc26";
				//graph.fillAlphas = 0.3; // setting fillAlphas to > 0 value makes it area graph
                graph.bulletSize = 3; // bullet image should be a rectangle (width = height)
                chart.addGraph(graph);

				var graph = new AmCharts.AmGraph();
                graph.type = "line";
                graph.valueField = "temp2";
                graph.lineColor = "#F2304D";
                graph.negativeLineColor = "#3053F2";
                //graph.fillAlphas = 0.3; // setting fillAlphas to > 0 value makes it area graph
				graph.bulletSize = 3; // bullet image should be a rectangle (width = height)
                chart.addGraph(graph);

				// CURSOR
				var chartCursor = new AmCharts.ChartCursor();
				chartCursor.cursorPosition = "mouse";
				chartCursor.categoryBalloonDateFormat = "JJ:NN, DD MMMM";
				chart.addChartCursor(chartCursor);

                // WRITE
                chart.write("chartdiv");
            });
		</script>

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
