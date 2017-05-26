angular.module("GFormsController", []).controller("appCtrl", function($scope, $mdDialog,apiService,$state) {
    $scope.app = {}
    $scope.app.isLogin = false;

    apiService.getData('answertype', {}, 'get').then(function(success) {
    // console.log(JSON.stringify(success.data))
        if (success.data.status == 200) {
            $scope.app.answer_type = success.data.type
            $scope.app.all_forms = success.data.all_forms
        } else {
            
        }
    });

    $scope.login = function(page_name) {
        $mdDialog.show({
            templateUrl: 'static/templates/login.html',
            controller: 'loginCtrl',
            locals: {
                page: '',
            },
            fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
        });
    }

    $scope.allform = function() {
        $state.go("app.form")
    }
    $scope.yourform = function() {
        $state.go("app.yourform")
    }

    $scope.$on("loggedIn", function(event, data) {
        user_detail_data = localStorage.getItem('UserObject')
        if (user_detail_data != null) {
            user_detail = JSON.parse(user_detail_data)
            $scope.app.isLogin = true;
            $scope.app.EmailID = user_detail.email;
            $scope.app.name = user_detail.first_name;
        }
    })

    if (localStorage.auth_token) {
        user_detail = JSON.parse(localStorage.getItem('UserObject'))
        if(user_detail){
            $scope.app.isLogin = true;
            $scope.app.EmailID = user_detail.email;
            $scope.app.avataar = user_detail.correct_image;
            $scope.app.name = user_detail.first_name;
        }
        
    }


    $scope.logout = function() {
        $scope.app.isLogin = false;
        localStorage.loginType = "none";
        localStorage.removeItem('auth_token');
        localStorage.removeItem('userId');
        localStorage.removeItem('UserObject')
        localStorage.userId = null
        $state.go("app.home");
    }

});
