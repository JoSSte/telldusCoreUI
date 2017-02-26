var lightsApp = angular.module('lightsApp', ['ui.bootstrap','angular-loading-bar']);
lightsApp.controller('DeviceListCtrl', function ($scope, $http, $interval) {
 $scope.loadData = function(){
   console.log("Load Called @"+ (new Date()));
   $scope.status = "Loading Device data";
   $http.get('tdaction.php?action=listDevices').success(function(data) {
     $scope.devices = data;
     $scope.status = "";
     console.log("Device data fetched @"+ (new Date()))
   });
 $scope.reloadSensors();
 };

 $scope.reloadSensors = function(){
  $scope.status = "Loading Sensor data";
   $http.get('tdaction.php?action=listSensors').success(function(data) {
     $scope.sensors = data;
     $scope.status = "";
     console.log("Sensor data fetched @"+ (new Date()))
   });
 };
 
 $scope.tdaction = function(id,action) {
   $scope.status = "Turning "+action+" Reloading Data" ;
   $http.get("tdaction.php?id="+id+"&action="+action);
   $scope.loadData();
 };
 
 $scope.allOff = function(){
   $http.get("tdaction.php?action=allOff");
   $scope.loadData();
 };
 $scope.orderProp = 'id';
 $interval($scope.reloadSensors, 45000);
});
lightsApp.filter('percentage', ['$filter', function ($filter) {
  return function (input) {
    if(input > 0){
      return input + '%';
    }else {
      return '';
    }
  };
}]);
lightsApp.filter('degree', ['$filter', function ($filter) {
  return function (input) {
    if(input > 0){
      return input + '°';
    }else {
      return '';
    }
  };
}]);

