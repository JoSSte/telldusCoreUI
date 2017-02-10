<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.9/angular.min.js"></script>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="style/lights.css">
    <script src="js/ui-bootstrap-tpls-2.5.0.min.js"></script>
    <script src="js/lights.js"></script>
    <title>lights</title>
</head>
<body>
<nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="">Lights</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Control</a></li>
            <!-- <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li> -->
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
        <div class="starter-template">
            <div ng-app = "lightsApp" ng-controller="DeviceListCtrl" data-ng-init="loadData()">

              <table ng-table="devicesTable" class="table table-striped">
                <thead>
                  <tr>
                    <th class="ng-hide">ID</th>
                    <th>Name</th>
                    <th>Last CMD</th>
                    <th colspan="2" class="center">Commands</th>
                  </tr>
                </thead>
                <tbody>
                  <tr ng-repeat="x in devices">
                    <td class="ng-hide">{{x.id}}</td>
                    <td>{{x.name}}</td>
                    <td>{{x.lastcommand}}</td>
                    <td><button class="btn btn-success" ng-click="tdaction(x.id,'on')">ON</button></td>
                    <td><button class="btn btn-danger" ng-click="tdaction(x.id,'off')">OFF</button></td>
                  </tr>
               </tbody>
             </table>
           <!-- todo: turn off all button -->
        <button type="button" class="btn btn-primary btn-danger" ng-click="allOff()">All OFF</button>
   {{status}}
        </div>
      </div>
    </div>
</body>
</html>
