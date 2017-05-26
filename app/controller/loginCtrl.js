angular.module("GFormsController").controller("loginCtrl", function($rootScope, $scope,  $state, apiService, $mdDialog,$timeout,page) {
    $scope.obj = {};
    $scope.landingPage = false;
    $scope.loginPage = false;
    $scope.registerPage = false;
    $scope.page = page
     if ($scope.page == "login") {
        $scope.loginPage = true;
    } else if ($scope.page == "signup") {
        $scope.registerPage = true;
    }else {
        $scope.landingPage = true;
    }
    $scope.obj.loginClick = function() {
        $mdDialog.hide()
        $mdDialog.show({
            templateUrl: 'static/templates/login.html',
            controller: 'loginCtrl',
            locals: {
                page: "login"
            },
            fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
        });
    }
    $scope.obj.signUpClick = function() {
        $mdDialog.hide()
        $mdDialog.show({
            templateUrl: 'static/templates/login.html',
            controller: 'loginCtrl',
            locals: {
                page: "signup"
            },
            fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
        });
    }


    var emailRegex = (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/);
    var phoneRegex = /^(\+\d{1,3}[- ]?)?\d{10}$/
    var nameRegex = /^[a-zA-Z ]{2,32}$/
    //*********************Form VAlidation Start *************************//
    $scope.obj.firstNameValidation = function() {
        if ($scope.obj.first_name == "" || $scope.obj.first_name == undefined || $scope.obj.first_name == null) {
            $scope.obj.firstnameErr = "Please enter your first name";
        } else if (!nameRegex.test($scope.obj.first_name))
            $scope.obj.firstnameErr = "Please enter a valid first name. A name should not contain special characters or numbers and is between 2-32 characters."
        else {
            $scope.obj.firstnameErr = null;
        }
    }

    $scope.obj.emailValidation = function() {
        if ($scope.obj.signupEmail == "" || $scope.obj.signupEmail == undefined || $scope.obj.signupEmail == null) {
            $scope.obj.signupEmailErr = "Please enter your email address";
        } else if (!emailRegex.test($scope.obj.signupEmail)) {
            $scope.obj.signupEmailErr = "Please enter valid email address";
        } else if ($scope.obj.signupEmail.length > 150) {
            $scope.obj.signupEmailErr = "Please enter a shorter email, if one is available.  If not, please email hello@avaana.com.au for assistance.";
        } else {
            $scope.obj.signupEmailErr = null;
        }

    }
    $scope.obj.passwordValidation = function() {
        if ($scope.obj.signupPassword == "" || $scope.obj.signupPassword == undefined || $scope.obj.signupPassword == null) {
            $scope.obj.signupPasswordErr = "Please enter a password";
        } else if ($scope.obj.signupPassword.length > 50 || $scope.obj.signupPassword.length < 7) {
            $scope.obj.signupPasswordErr = "Please enter a password between 8 and 24 characters.";
        } else {
            $scope.obj.signupPasswordErr = null;
        }

    }


    //**Validate button Listener ********
    $scope.obj.signup = function() {
        $scope.obj.firstNameValidation()
        $scope.obj.emailValidation()
        $scope.obj.passwordValidation()
        if ($scope.obj.signupEmailErr == null && $scope.obj.signupPasswordErr == null && $scope.obj.firstnameErr == null) {
            data = {
                first_name: $scope.obj.first_name,
                email: $scope.obj.signupEmail,
                password: $scope.obj.signupPassword,
            }
            apiService.getData('signup', data, 'post').then(function(success) {
                if (success.data.status == 200) {
                    localStorage.setItem('UserObject',JSON.stringify(success.data.User_Detail));
                    localStorage.auth_token = success.data.auth_token
                    $rootScope.$broadcast('loggedIn');
                    $mdDialog.hide()
                    $scope.obj.signupEmailErr = null;
                } else if (success.data.status == 500) {
                    error_key = Object.keys(success.data.Message);
                    if (error_key[0] === 'email') {
                        $scope.obj.signupEmailErr = "Email address already exists.  Did you mean to log in instead?";
                    } else if (error_key[0] === 'password') {
                        $scope.obj.signupPasswordErr = "Password is too short.";
                    } else {
                        $scope.obj.phoneErr = success.data.Error;
                    }
                }
            }, function(error) {
            });
        }
    }

    //*******************************End register Section*************************


    $scope.obj.login = function() {
        if ($scope.obj.email == "" || $scope.obj.email == undefined || $scope.obj.email == null) {
            $scope.obj.emailErr = "Please enter a valid email.";
        } else if (!emailRegex.test($scope.obj.email)) {
            $scope.obj.emailErr = "Please enter a valid email.";
        } else {
            $scope.obj.emailErr = null;
        }
        if ($scope.obj.password == "" || $scope.obj.password == undefined || $scope.obj.password == null) {
            $scope.obj.passwordErr = "Please enter a password.";
        } else {
            $scope.obj.passwordErr = null;
        }
        if ($scope.obj.emailErr == null && $scope.obj.passwordErr == null) {
            localStorage.loginType = "normal";

            data = {
                    email: $scope.obj.email,
                    password: $scope.obj.password
                }
            apiService.getData('login', data, 'post').then(function(success) {
                if (success.data.status != 500) {
                    localStorage.userId = success.data.user.id
                    localStorage.auth_token = success.data.auth_token
                    localStorage.setItem('UserObject',JSON.stringify(success.data.user));
                    $rootScope.$broadcast('loggedIn');
                    $mdDialog.hide()

                    $scope.obj.loginErr = null;
                } else {
                    $timeout($scope.obj.failureErr = "Incorrect email or password.", 500);
                }
            }, function(error) {
                $scope.obj.failureErr = "Oops, something went wrong: " + error.status;
            });
        }
    }
    $scope.obj.loginEmailValidate=function(){
       if ($scope.obj.email == "" || $scope.obj.email == undefined || $scope.obj.email == null) {
              $scope.obj.emailErr = "Please enter a valid email.";
          } else if (!emailRegex.test($scope.obj.email)) {
              $scope.obj.emailErr = "Please enter a valid email.";
          } else {
              $scope.obj.emailErr = null;
          }
    }

    $scope.obj.loginPasswordValidate=function(){
         if ($scope.obj.password == "" || $scope.obj.password == undefined || $scope.obj.password == null) {
                $scope.obj.passwordErr = "Please enter a password.";
            } else {
                $scope.obj.passwordErr = null;
            }
    }
    $scope.obj.closeClick = function() {
        $mdDialog.hide()
    }




});