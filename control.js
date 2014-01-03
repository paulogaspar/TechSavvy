var tsApp = angular.module('tsApp', []);

tsApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

tsApp.controller('tsController', function($scope, $http, $window, $timeout)
{
	$scope.contentCache = undefined;
	$scope.allContent = "Loading content..."
	$scope.go = function(){
		$window.open( "https://www.facebook.com/groups/tech.savvyness/permalink/"+ this.post.id.split('_')[1]+"/" );
	}

	$http.get('/getcontent/json')
		 .success(function(response) {
		 		$scope.contentCache = response;
        		$scope.allContent = response;
        		angular.forEach(response, function (_tmpitem, idx) {
        			$timeout(function(){
        				if(_tmpitem.picture==undefined){
	        				$http.get('/api/fetchImage?url='+_tmpitem.link).success(function(response){
	        					if(response!=''){
	        						_tmpitem.picture = response;
	        					}
							});
	        			}

	        			if(_tmpitem.message==undefined){
	        				$http.get('/api/fetchDescription?url='+_tmpitem.link).success(function(response){
	        					if(response!=''){
	        						_tmpitem.message = response;
	        					}
							});
	        			}

        			})
        		});
    });
})
.directive('jsFloatLable', function() {
    var linkFn;
    linkFn = function($scope, $element, $attrs) {
        jQuery($element[0]).FloatLabel();
    };
    return {
        restrict: 'A',
        link: linkFn
    };
});;