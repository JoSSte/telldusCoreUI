<?php
//TODO: sanitize inputs
//TODO: return response codes
//TODO: allowmultiple ids/device groups

// https://lassesunix.wordpress.com/2013/12/28/decoding-nexa-remotes-with-tellstick-duo/
$action = $_GET["action"];
$id = $_GET["id"];

switch ($action){
  case "on":
  case "off":
    $cmd = "tdtool --$action $id";
    exec($cmd);
    error_log($cmd." executed");
    break;
  case "listDevices":
    header("Content-Type: application/json");
    //return JSON
    echo json_encode(getAllDevices());
    break;
  case "listSensors":
    header("Content-Type: application/json");
    //return JSON
    echo json_encode(getAllSensors());
    break;
  case "allOff":
    $alldevs = getAllDevices();
    foreach($alldevs as $dev){
      exec("tdtool --off ".$dev["id"]);
    }
    break;

}


function getAllDevices(){
  //TODO: investigate multi threaded activity here: http://stackoverflow.com/questions/70855/how-can-one-use-multi-threading-in-php-applications
  //get devices from tdtool
  $devs = shell_exec("tdtool --list-devices");

  //turn raw result into array
  $devicelist = array();
  preg_match_all('/type=(?<type>\w+)\tid=(?<id>\d+)\tname=(?<name>[a-zA-ZæøåÆØÅ\-]+)\tlastsentcommand=(?<lastcommand>\w+)/', $devs, $matches);
  for ($x = 0 ; $x < count($matches[0]);$x++){
    $devicelist[] = array("id"=> $matches["id"][$x],"name"=>$matches["name"][$x],"lastcommand"=>$matches["lastcommand"][$x]);
  }
  return $devicelist;
}

function getAllSensors(){
  //get devices from tdtool
  $sens = shell_exec("tdtool --list-sensors");

  //turn raw result into array
  $sensorlist = array();
  preg_match_all('/type=(?<type>\w+)\tprotocol=(?<protocol>\w+)\tmodel=(?<model>\w+)\tid=(?<id>\d+)\ttemperature=(?<temperature>[\d\.]+)(|\thumidity=(?<humidity>[\d\.]+))\ttime=(?<time>[\d-\s:]+)\tage=(?<age>\d+)/', $sens, $matches);
  for ($x = 0 ; $x < count($matches[0]);$x++){
    $sensorlist[] = array("type"=> $matches["type"][$x],"protocol"=>$matches["protocol"][$x],"id"=>$matches["id"][$x],"temperature"=>$matches["temperature"][$x],"humidity"=>$matches["humidity"][$x],"time"=>$matches["time"][$x],"age"=>$matches["age"][$x]);
  }
  return $sensorlist;
}

