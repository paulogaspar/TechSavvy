var tsApp = angular.module('tsApp', []);

tsApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});


tsApp.controller('tsController', function($scope, $http)
{
	$scope.allContent = "Loading content..."

	$http.get('http://localhost:8080/getcontent/json').success(function(response) {
        console.log(response[0]["picture"]);
        $scope.allContent = response;
    });

       /*.then(function(res){
          $scope.allContent = res.data;                
        });*/
});