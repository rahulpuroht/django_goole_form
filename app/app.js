angular.module('myApp', [
    'ngMaterial',
    'ui.router',
    'GFormsController',
    "GFormsService",
]).constant('apiUrl', 'http://0.0.0.0:3000/')
.config(['$stateProvider', '$urlRouterProvider', '$httpProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $httpProvider, $locationProvider) {
    $stateProvider
        .state('app', {
            url: "/app",
            views: {
                "main": {
                    templateUrl: "static/templates/app.html",
                    controller: "appCtrl"
                }
            }
        })
    .state('app.home', {
        url: "/home",
        views: {
            "content": {
                templateUrl: "static/templates/home.html",
                controller: "homeCtrl"
            }
        }
    })

    .state('app.form', {
        url: "/allform",
        views: {
            "content": {
                templateUrl: "static/templates/allform.html",
                controller: "formCtrl"
            }
        }
    })
    .state('app.yourform', {
        url: "/yourform",
        views: {
            "content": {
                templateUrl: "static/templates/yourform.html",
                controller: "yourformCtrl"
            }
        }
    })
    $urlRouterProvider.otherwise("/app/home");
}]);