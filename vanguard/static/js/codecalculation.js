var app_common = {
    data: {
        userAuthenticated : false,
        username: '',
        message: "",
        messageType: "",
        messageIsActive: false,
        schemaErrors : {},
        errorStatus : {}
    },

    computed : {
      messageClass : function(){
        cls = { 'is-warning' : this.messageType=='warning', 'is-danger': this.messageType=='error', 'is-success': this.messageType=='success'};
        return cls;
      }
    },

    methods : {

        openModal: function(modalisActive) {
            this[modalisActive] = true;
            this.reset_message();
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');
        },

        closeModal: function(modalisActive) {
            this[modalisActive] = false;
            this.reset_message();
        },

        hide_message: function() {
            this.messageIsActive = false;
        },

        reset_message: function() {
            this.message = "";
            this.messageType = "";
            this.messageIsActive = false;
            this.schemaErrors = {}
        },

        store_message : function(){
            localStorage["message"] = this.message;
            localStorage["messageType"] = this.messageType;
            localStorage["messageIsActive"] = this.messageIsActive;
        },

        retrieve_message : function(){
            this.message = localStorage["message"];
            this.messageType = localStorage["messageType"];
            if (localStorage["messageIsActive"] =="true"){
                this.messageIsActive = true;
            }
            else{
                this.messageIsActive = false;
            };
        },

        login: function(){
            var app = this;
            app.reset_message();
            var data = {};
            data.username = app.username;
            data.password = app.password;
            var json_data = JSON.stringify(data);
            url = "/auth/";
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    response = JSON.parse(xhr.responseText);
                    app.userAuthenticated = true;
                    localStorage.setItem('access_token', response['access_token']);
                    // use the token received to perform a basic authentication on login test. Browser will rememeber the Credentials
                    // for all future requests and dispatch tokens automatically.
                    url = "/login-test/";
                    token = localStorage["access_token"];
                    var xhr2 = new XMLHttpRequest();
                    xhr2.open("GET", url, true, token, "unused");
                    xhr2.onload = function (e) {
                      if (xhr2.readyState === 4) {
                        if (xhr2.status === 200) {
                            localStorage.setItem('username', app.username);
                            localStorage.setItem('userAuthenticated', app.userAuthenticated);
                            app.message = "User successfully logged in";
                            app.messageType = "success"
                            app.messageisActive = true;
                            app.loginModalisActive = false;
                            location.href = "/profile";
                        } else {
                          console.error(xhr2.statusText);
                          app.message = "Login Failed.";
                          app.messageType = "error"
                          app.messageisActive = true;
                        }
                      }
                    };
                    xhr2.onerror = function (e) {
                      console.error(xhr2.statusText);
                      app.message = "Login Failed.";
                      app.messageType = "error"
                      app.messageisActive = true;
                    };
                    xhr2.send(null);
                }
                else{
                    app.userAuthenticated = false;
                    localStorage.setItem('access_token', 'anonymous');
                    localStorage.setItem('username', app.username);
                    localStorage.setItem('userAuthenticated', app.userAuthenticated);
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(json_data);
        },

        logout: function(){
            var app = this;
            app.reset_message();
            localStorage.setItem('access_token', 'anonymous');
            localStorage.setItem('username', '');
            localStorage.setItem('userAuthenticated', false);
            token = localStorage["access_token"];
            app.username = localStorage["username"];
            if (localStorage["userAuthenticated"]=="true"){
                app.userAuthenticated = true;
            }
            else{
                app.userAuthenticated = false;
            }
            url = "/login-test/"
            var xhr = new XMLHttpRequest();
            xhr.open("GET", url, true, token, "unused");
            xhr.onload = function (e) {
              if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    app.message = "Logout Failed.";
                    app.messageType = "error"
                    app.messageisActive = true;
                } else {
                  console.error(xhr.statusText);
                  location.href = "/index/";
                }
              }
            };
            xhr.onerror = function (e) {
              console.error(xhr.statusText);
            };
            xhr.send(null);
        },

        load_protected: function(url){
            token = localStorage["access_token"];
            if (typeof token === "undefined") {
                token = "anonymous";
              }
            var xhr = new XMLHttpRequest();
            xhr.open("GET", url, true, token, "unused");
            xhr.onload = function (e) {
              if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    console.log(xhr.responseText);
                    document.location.pathname = url;
                } else {
                    app.message = xhr.statusText;
                    app.messageType = "error"
                    app.messageisActive = true;
                    console.error(xhr.statusText);
                }
              }
            };
            xhr.onerror = function (e) {
              console.error(xhr.statusText);
            };
            xhr.send(null);
        }, //end of loadProtectedResource

        get_resource_list : function(resource_list, base_url, fn_success) {
            var app = this;
            app.reset_message();
            url = base_url;
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    app.handle_success_with_content(xhr, resource_list);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(null);
        },


        get_resource: function(resource_name, resource_id, base_url, fn_success) {
            var app = this;
            app.reset_message();
            url = base_url + resource_id + "/";
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    app.handle_success_with_content(xhr, resource_name);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(null);
        },


        add_resource: function(resource_name, base_url, fn_success) {
            var app = this;
            app.reset_message();
            url = base_url;
            var data = {};
            data.resource = app[resource_name];
            var json_data = JSON.stringify(data);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            app.isLoading = true;
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "201"){
                    app.handle_success_without_content(xhr);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(json_data);
        },


        update_resource: function(resource_name, resource_id, base_url, fn_success) {
            var app = this;
            app.reset_message();
            url = base_url + resource_id + '/'
            var data = {};
            data.resource = app[resource_name];
            var json_data = JSON.stringify(data);
            var xhr = new XMLHttpRequest();
            xhr.open('PUT', url, true);
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            xhr.onload = function(e){
                console.log(xhr.responseText);
                if (xhr.readyState == 4 && xhr.status == "200"){
                    app.handle_success_without_content(xhr);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(json_data);
        },

        delete_resource: function(resource_name, resource_id, base_url, fn_success) {
            if (confirm("Want to delete " + resource_id + " in " + resource_name)) {
                var app = this;
                app.reset_message();
                url = base_url + resource_id + '/';
                var xhr = new XMLHttpRequest();
                xhr.open('DELETE', url, true);
                xhr.onload = function(e){
                    if (xhr.readyState == 4 && xhr.status == "200"){
                        app.handle_success_without_content(xhr);
                        fn_success();
                    }
                    else{
                        app.handle_errors(xhr);
                    }
                };
                xhr.onerror = function (e) {
                    app.handle_connection_errors();
                };
                xhr.send(null);
            }
        },

        process_resource: function(resource_name, base_url, fn_success) {
            var app = this;
            app.reset_message();
            url = base_url;
            var data = {};
            data[resource_name] = app[resource_name];
            var json_data = JSON.stringify(data);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            app.isLoading = true;
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    app.handle_success_with_content(xhr, resource_name);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(json_data);
        },

        handle_success_with_content : function(xhr, resource_name){
            console.log(xhr.responseText);
            response = JSON.parse(xhr.responseText);
            this[resource_name] = response;
            this.message = "Data Loaded Successfully"
            this.messageType = 'success'
            this.isLoading = false;
        },

        handle_success_without_content : function(xhr){
            console.log(xhr.responseText);
            response = JSON.parse(xhr.responseText);
            if (response.hasOwnProperty("message")){
              this.message = response["message"];
            }
            else{
              this.message = xhr.statusText;
            }
            this.messageType = 'success'
            this.isLoading = false;
            if (response.hasOwnProperty("redirect_url")){
                location.href = response["redirect_url"];
            }
        },


        handle_errors : function(xhr){
            console.error(xhr.response);
            this.errorStatus = xhr.status + " " + xhr.statusText;
            try {
                response = JSON.parse(xhr.responseText);
                if (response.hasOwnProperty("message")){
                  this.message = response["message"];
                }
                else{
                  this.message = xhr.responseText;
                }
                if (response.hasOwnProperty("schemaErrors")){
                  this.schemaErrors = response["schemaErrors"];
                }
                else{
                  this.schemaErrors = {};
                }
            }
            catch (e) {
                this.message = xhr.response;
            }
            this.messageType = 'error'
            this.messageIsActive = true;
            this.isLoading = false;
        },

        handle_connection_errors : function(){
            this.errorStatus = "Unknown Error";
            this.message = "Server Response not received";
            this.messageType = 'error'
            this.messageisActive = true;
            this.isLoading = false;
        },


        addListItem: function(targetList, list_entry) {
            var lsitem = JSON.parse(JSON.stringify(list_entry));
            targetList.push(lsitem);
        },

        removeListItem: function(targetList, index) {
            targetList.splice(index, 1);
        },

        retSilent: function(obj, path_array) {
            val = obj;
            total_length = path_array.length;
            try{
                for (i = 0; i < total_length; i++) {
                    key = path_array[i];
                    val = val[key];
                }
                return val;
            }
            catch (err) {
                return "";
            }
        },


        launchHelp : function(){
          hurl = this.help_url;
          if (hurl==null){
            hurl = 'http://docs.codecalculation.com/'
          }
          window.open(hurl, 'helpwindow',"height=640,width=960,toolbar=no,menubar=no,scrollbars=no,location=no,status=no");
        },


    },

    beforeMount : function(){
      try{
        this.username = localStorage['username'];
        if (localStorage.getItem("userAuthenticated")=="true"){
              this.userAuthenticated = true;
          }
          else{
              this.userAuthenticated = false;
          }
      }
      catch (e){
        this.username = "";
        this.userAuthenticated = false;
      }
    },



}
