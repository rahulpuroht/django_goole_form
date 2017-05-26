angular.module("GFormsController").controller("homeCtrl", function($scope, $state, apiService) {
    $scope.obj = {}
    $scope.obj.form_question = false
    $scope.save_form = function() {
        if ($scope.obj.form_name == "" || $scope.obj.form_name == undefined || $scope.obj.form_name == null) {
            $scope.obj.form_nameErr = "Please enter a valid Form Name.";
        } else {
            $scope.obj.form_nameErr = null;
        }
        if ($scope.obj.form_nameErr == null) {
            data = {
                form_name: $scope.obj.form_name,
                form_description: $scope.obj.form_description,
            }
            apiService.getDataWithToken('addform', data, 'post').then(function(success) {
                console.log(success.data)
                if (success.data.status == 200) {
                    $scope.obj.failureErr = null;
                    $scope.obj.form_question = true
                    $scope.question_id = success.data['id']
                } else if (success.data.status == 500) {
                    $scope.obj.failureErr = success.data.error
                }
            }, function(error) {});
        }
    }
    $scope.items = ["A", "B", "C", "D"];
    $scope.selected = [];
    $scope.exists = function(item, list) {
        return list.indexOf(item) > -1;
    };

    $scope.toggle = function(item, list) {
        var idx = list.indexOf(item);
        if (idx > -1) {
            list.splice(idx, 1);
        } else {
            list.push(item);
        }
    };

    $scope.question_Array = []
    $scope.save_question = function() {
        if ($scope.obj.question == "" || $scope.obj.question == undefined || $scope.obj.question == null) {
            $scope.obj.questionErr = "Please enter a question.";
        } else {
            $scope.obj.questionErr = null;
        }
        if ($scope.obj.questionErr == null) {
            data = {
                form_id: $scope.question_id,
                question: $scope.obj.question,
                answer_type : $scope.obj.type
            }
            console.log(JSON.stringify(data))
            apiService.getDataWithToken('addquestion', data, 'post').then(function(success) {
                console.log(success.data)
                if (success.data.status == 200) {
                    $scope.question_Array = success.data.question
                    $scope.question = false
                } else if (success.data.status == 500) {
                    $scope.obj.failureErr = success.data.error
                }
            }, function(error) {});
        }
    }
});