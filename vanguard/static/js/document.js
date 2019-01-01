var app_doc = {
    data: {
      unitsModalisActive: false,
      uploadModalisActive: false,
      loadingModalisActive: false,


    },
    computed : {
      url_subpath : function(){
        return window.location.pathname.slice(4);
      },

      dimensions_used: function() {
          dimensions = []
          for (var dimension in this.doc.units) {
              if (this.doc.units.hasOwnProperty(dimension)) {
                  dimensions.push(dimension);
              }
          }
          return dimensions;
      },
      units_used : function(){
        var clone = JSON.parse(JSON.stringify(this.doc.units))
        return clone;
      }
    },
    watch: {
      'units_used': {
          handler: function(new_units, old_units) {
              try {
                 this.treeUnitConvert(this.doc, old_units, new_units);
              } catch (err) {
                  console.log("Error in watch handler for units_used");
              }
          },
          deep: true,
      }
    },
    methods : {

      saveDoc: function() {
          mydata = JSON.stringify(this.doc, null, 2);
          save_anchor = this.$refs['save_anchor']
          save_anchor.download = "formData-" + new Date().getTime();
          save_anchor.href = "data:text/plain," + encodeURIComponent(mydata);
          save_anchor.click();
      },

      calculate : function(){
          fn_success =function(){};
          this.doc['result'] ={};
          this.doc['errors'] =[];
          calculation_url = "/api"+ this.url_subpath;
          this.process_resource("doc", calculation_url, fn_success);
      },

      pdf_download: function() {
          var app = this;
          app.reset_message();
          pdf_url = "/pdf"+ this.url_subpath;

          var data = {};
          data['doc'] = app['doc'];
          var json_data = JSON.stringify(data);
          var xhr = new XMLHttpRequest();
          xhr.open('POST', pdf_url, true);
          xhr.responseType = "arraybuffer";
          xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
          app.loadingModalisActive =true;

          xhr.onload = function(e){
              if (xhr.readyState == 4 && xhr.status == "200"){
                  var blob = new Blob([xhr.response], {type: "application/pdf"});
                  var link = document.createElement('a');
                  link.href = window.URL.createObjectURL(blob);
                  link.download = 'PDF Report.pdf';
                  link.click();
                  app.loadingModalisActive =false;
              }
              else{
                  app.errorStatus = xhr.status + " " + xhr.statusText;
                  app.errorMessage = "Error occured in PDF Download"
                  app.errorisActive = true;
                  app.isLoading = false;
                  app.loadingModalisActive =false;
              }
          };
          xhr.onerror = function (e) {
              xhr.responseType = "text";
              app.handle_connection_errors();
              app.loadingModalisActive =false;
          };
          xhr.send(json_data);
      },

      launch_help : function(){
        help_url = "/static"+ this.url_subpath + "help.html";
        window.open(help_url, 'helpwindow',"height=640,width=960,toolbar=no,menubar=no,scrollbars=no,location=no,status=no");
      },


      getErrs: function(path_array) {
          try{
              var app = this;
              xval = this.retSilent(app['schemaErrors']['input'], path_array);
              if (xval instanceof Array){
                   return xval
                 }
              else {return []}
           }
           catch (err) {
               return [];
           }
         },


      getResult: function(path_array) {
          try{
             var app = this;
              xval = this.retSilent(app['doc']['result'], path_array);
             if (typeof xval ==='object'){
                if (xval.hasOwnProperty("_val") ){
                  return xval['_val']
                }
                else {return ""}
              }
              else{
                return xval;
              }
          }
          catch (err) {
              return "";
          }
      },

      gUL: function(dimension) {
          try {
              unitUsed = this.doc.units[dimension]
              unitLabel = getUnitLabel(dimension, unitUsed)
              return unitLabel
          } catch (err) {
              console.log("Error occured in getUnitLabel trying to fetch unitUsed '" + unitUsed + "'")
              return '';
          }
      },

      getUnits: function(dimension) {
          try {
              return getUnits(dimension)
          } catch (err) {
              console.log("Error occured in getUnits with dimension = '" + dimension + "'");
          }
      },

      treeUnitConvert : function(tree, fromUnits, toUnits){
          treeUnitConvert(tree, fromUnits, toUnits);
      }

    }
}
