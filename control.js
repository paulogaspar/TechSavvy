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
        		for(var i = 0; i < response.length; i++){
        			$scope.$apply(function(){
        				var _tmpitem = response[i];
	        			if(_tmpitem.picture==undefined){
	        				$http.get('/api/fetchImage?url='+_tmpitem.link).success(function(response){
	        					if(response!=''){
	        						console.log('item:',_tmpitem.name,' <-> og:image:',response);	
	        						_tmpitem.picture = response;
	        					}
							});
	        			}
        			})
        		}
    });
});