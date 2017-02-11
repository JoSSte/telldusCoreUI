var lightsApp = angular.module('lightsApp', ['ui.bootstrap','angular-loading-bar']);

lightsApp.controller('DeviceListCtrl', function ($scope, $http) {
 $scope.loadData = function(){
   //console.log("Load Called");
   $scope.status = "Loading data";
   $http.get('tdaction.php?action=listDevices').success(function(data) {
     $scope.devices = data;
     $scope.status = "";
   });
 };

 $scope.tdaction = function(id,action) {
   $scope.status = "Turning "+action+" Reloading Data" ;
   //console.log(id + " "+ action);
   $http.get("tdaction.php?id="+id+"&action="+action);
   $scope.loadData();
   $scope.status ="";
 };
 
 $scope.allOff = function(){
   $http.get("tdaction.php?action=allOff");
   $scope.loadData();
 };
 $scope.orderProp = 'id';

});

