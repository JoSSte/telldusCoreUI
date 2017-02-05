<?php
//TODO: sanitize inputs
//TODO: return response codes
//TODO: allowmultiple ids/device groups
$action = $_GET["action"];
$id = $_GET["id"];

switch ($action){
  case "on":
  case "off":
    $cmd = "tdtool --$action $id";
    shell_exec($cmd);
    error_log($cmd." executed");
    break;
  case "listDevices":
    header("Content-Type: application/json");
    //return JSON
    echo json_encode(getAllDevices());
    break;
  case "allOff":
    $alldevs = getAllDevices();
    foreach($alldevs as $dev){
      shell_exec("tdtool --off ".$dev["id"]);
    }
    break;

}


function getAllDevices(){
  //get devices from tdtool
  $devs = shell_exec("tdtool --list-devices");

  //turn raw result into array
  $devicelist = array();
  preg_match_all('/type=(?<type>\w+)\tid=(?<id>\d+)\tname=(?<name>[a-zA-ZæøåÆØÅ\-]+)\tlastsentcommand=(?<lastcommand>\w+)/', $devs, $matches);
  for ($x= 0 ; $x < count($matches[0]);$x++){
    $devicelist[] = array("id"=> $matches["id"][$x],"name"=>$matches["name"][$x],"lastcommand"=>$matches["lastcommand"][$x]);
  }
  return $devicelist;
}
