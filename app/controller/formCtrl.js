angular.module("GFormsController").controller("formCtrl", function($scope, $state, apiService) {


    apiService.getData('allforms', {}, 'get').then(function(success) {
        if (success.data.status == 200) {
            $scope.all_forms = success.data.all_forms
        } else {

        }
    });

    $scope.items = ["A", "B", "C", "D"];
    $scope.selected = [];
    $scope.exists = function(item, list) {
        return list.indexOf(item) > -1;
    };
    $scope.form_response = {}
    $scope.toggle = function(item, list,form_question) {
        console.log(form_question.question)
        var idx = list.indexOf(item);
        if (idx > -1) {
            list.splice(idx, 1);
        } else {
            list.push(item);
        }
        form_question['response'] = true
        form_question['answere'] = list.toString()
        form_question['form'] = form_question['form_id']
        form_question['question_id'] = form_question['id']
    };
    $scope.form_det = {}
    $scope.form_Select = function(form) {
        $scope.form_det = {}
        $scope.selected = []
        $scope.form_det = form['form_details']
    }

    $scope.selectedResponse = function(form_question, response) {
        form_question['response'] = true
        form_question['answere'] = response
        form_question['form'] = form_question['form_id']
        form_question['question_id'] = form_question['id']
    }

    $scope.save_response = function() {
        apiService.getData('saveResponse', $scope.form_det, 'post').then(function(success) {
            console.log(success.data)
            if (success.data.status == 200) {
                $scope.form_det = {}
                $scope.selected = [];
            } else {

            }
        });

    }
});