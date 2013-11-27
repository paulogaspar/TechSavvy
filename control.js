var tsApp = angular.module('tsApp', []);

tsApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

tsApp.controller('tsController', function($scope, $http, $window)
{
	$scope.allContent = "Loading content..."
	$scope.go = function(){
		$window.open( "https://www.facebook.com/groups/tech.savvyness/permalink/"+ this.post.id.split('_')[1]+"/" );
	}
	$http.get('/getcontent/json')
		 .success(function(response) {
        		$scope.allContent = response;
    });
});