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
    $scope.isURL = function(url) {
        if(url==undefined)
            return false;
        
        var strRegex = "^((https|http|ftp|rtsp|mms)?://)"
            + "?(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?" //ftp?user@
            + "(([0-9]{1,3}\.){3}[0-9]{1,3}" // IP???URL- 199.194.52.184
            + "|" // ??IP?DOMAIN(??)
            + "([0-9a-z_!~*'()-]+\.)*" // ??- www.
            + "([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\." // ????
            + "[a-z]{2,6})" // first level domain- .com or .museum
            + "(:[0-9]{1,4})?" // ??- :80
            + "((/?)|" // a slash isn't required if there is no file name
            + "(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$";
            
        /* /(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:;,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:;,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:;,.]*\)|[A-Z0-9+&@#\/%=~_|$])/i
        */
        var re=new RegExp(strRegex);
        return re.test(url.trim());
    }

	$http.get('/content/json')
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
});