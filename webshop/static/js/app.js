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

  $scope.addToCart = function(id) {
    // $http.post('/cart/', {"productId": id, "csrfmiddlewaretoken": CSRF_TOKEN})
    $http({
      url: "/api/cart/",
      method: "POST",
      data: {"productId": id},
      headers: {"X-CSRFToken": CSRF_TOKEN}
    }).then(function successCallback(response) {
      if(response.data.success === true) {
        toastr.success("Item added to cart!")
      }else{
        toastr.error("Something went wrong.")
      }
    })
  }
});

app.controller('CartController', function($scope, $http){
  $http.get('/api/cart/').then(function successCallback(response){
    let tempProducts = [];
    angular.forEach(response.data.products, function(item) {
        tempProducts.push(item)
    })
    $scope.products = tempProducts;
    $scope.grandTotal = response.data.balance.grandTotal;
    $scope.balanceAfterPurchase = response.data.balance.balanceAfterPurchase;
    $scope.sufficientFunds = response.data.balance.sufficientFunds;
    $scope.accountBalance = response.data.balance.accountBalance;
  }, function errorCallback(response) {
    error.log(response);
  })
});


// product.html not is use currently
app.controller('ProductController', function($scope, $http, $location){
  // TODO: Get rid of this disgusting solution
  var url = $location.absUrl();
  var id = url.substring(url.indexOf("=") + 1);

  $http.get('/api/product/'+id).then(function successCallback(response){
    $scope.product = response.data
  }, function errorCallback(response) {
    error.log(response);
  })
});


app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});
