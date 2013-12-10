var tsApp = angular.module('tsApp', []);

tsApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

tsApp.controller('tsController', function($scope, $http, $window)
{
	$scope.contentCache = undefined;
	$scope.allContent = "Loading content..."
	$scope.go = function(){
		$window.open( "https://www.facebook.com/groups/tech.savvyness/permalink/"+ this.post.id.split('_')[1]+"/" );
	}
	$scope.$watch('mSearch', function(query) {
		if($scope.contentCache==undefined)
			return;
		if(query==undefined || query==""){
			$scope.allContent = $scope.contentCache;
			return;	
		}
		$scope.allContent = $scope.contentCache.filter(function(item){
			console.log(item.message!=undefined && item.message.toLowerCase().indexOf(query.toLowerCase()) < 0);
			return item.message!=undefined && item.message.toLowerCase().indexOf(query.toLowerCase()) > 0;
		});
		console.log($scope.allContent.length);
	}, true);

	$http.get('/getcontent/json')
		 .success(function(response) {
		 		$scope.contentCache = response;
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

	        			if(_tmpitem.message==undefined){
	        				$http.get('/api/fetchDescription?url='+_tmpitem.link).success(function(response){
	        					if(response!=''){
	        						console.log('item:',_tmpitem.name,' <-> og:description:',response);	
	        						_tmpitem.message = response;
	        					}
							});
	        			}

        			})
        		}
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