var lightsApp = angular.module('lightsApp', ['ui.bootstrap','angular-loading-bar']);
lightsApp.controller('DeviceListCtrl', function ($scope, $http) {
 $scope.loadData = function(){
   console.log("Load Called @"+ (new Date()));
   $scope.status = "Loading data";
   $http.get('tdaction.php?action=listDevices').success(function(data) {
     $scope.devices = data;
     $scope.status = "";
     console.log("data fetched @"+ (new Date()))
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

});

