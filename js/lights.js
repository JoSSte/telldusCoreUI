var lightsApp = angular.module('lightsApp', ['ui.bootstrap']);   

lightsApp.controller('DeviceListCtrl', function ($scope, $http) {
 $http.get('tdaction.php?action=listDevices').success(function(data) {
   $scope.devices = data;
 });

 $scope.tdaction = function(id,action) {
   console.log(id + " "+ action);
   $http.get("tdaction.php?id="+id+"&action="+action);
   //todo: reload table
 };
 
 $scope.allOff = function(){
   $http.get("tdaction.php?action=allOff");
 };
 $scope.orderProp = 'id';

});

