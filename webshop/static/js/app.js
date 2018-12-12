app = angular.module('indexApp', [])

app.controller('AppController', function($scope, $http){
  $scope.activeCategory = -1;
  $scope.categories = [];
  $scope.products = [];

  $http.get('api/category/').then(function successCallback(response){
    angular.forEach(response.data, function(item) {
        $scope.categories.push(item)
    })
  }, function errorCallback(response) {
    error.log(response);
  })

  $http.get('api/product/').then(function successCallback(response){
    angular.forEach(response.data, function(item) {
        $scope.products.push(item)
    })
  }, function errorCallback(response) {
    error.log(response);
  })

  $scope.filterProducts = function(id) {
    $scope.activeCategory = id;
    $http({
      url: "api/product/",
      method: "GET",
      params: {"category_id": id}
    }).then(function successCallback(response){
      let tempProducts = [];
      angular.forEach(response.data, function(item) {
          tempProducts.push(item)
      })
      $scope.products = tempProducts;
    }, function errorCallback(response) {
      error.log(response);
    })
  }
});

app.controller('ProductController', function($scope, $http){
  $http.get('api/product/').then(function successCallback(response){

  }, function errorCallback(response) {
    error.log(response);
  })
});


app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});
