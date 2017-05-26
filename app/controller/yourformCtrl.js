angular.module("GFormsController").controller("yourformCtrl", function($scope, $state, apiService) {
    

	 apiService.getDataWithToken('yourforms', {}, 'get').then(function(success) {
        // console.log(JSON.stringify(success.data.your_forms))
        if (success.data.status == 200) {
            $scope.your_forms = success.data.your_forms
        } else {
            
        }
    });



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
    $scope.form_det = {}
    $scope.form_Select = function(form){
        $scope.response_sel = {}
    	$scope.form_det = form['form_details']
        $scope.form_res = form['form_response']
    }


    $scope.response_sel = {}
    $scope.response_Select = function(res){

        $scope.response_sel = {}
        $scope.response_sel = res['question_response']
         console.log(JSON.stringify(res))
    }
});