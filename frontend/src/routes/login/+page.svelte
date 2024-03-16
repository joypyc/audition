
<script>
    import {loggedUser, csrfToken} from '$lib/stores'
    import {loginUrl} from '$lib/config.js';
    import {getCookie} from "$lib/utils.js"
    import {goto} from "$app/navigation"

    import AlertBox from '$lib/components/AlertBox.svelte'
    let username;
    let password;
    let errorMsg;
    async function login(){
        try{
            // send authentication request to backend
            let res = await fetch(loginUrl,{
                "method": "POST",
                "credentials": "include",
                "headers": {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": getCookie('csrftoken')
                },
                "body": JSON.stringify({
                    "username": username,
                    "password": password
                })
            })
        
            if (res.ok){  //on success set loggedUser store
                let userData = await res.json()
                loggedUser.set({
                    "id": userData['id'],
                    "firstName": userData['first_name'],
                })
                goto('/')
            }
            else{
                let jsonData = await res.json()
                let errorRes = jsonData['error']
                errorMsg = errorRes
            }

        } catch(e){
            console.error(e)
            errorMsg = 'Unable to log in. Please try again later.'
        }
    }
</script>
<div class='form-container'>
<div class="row justify-content-center center">
    <div class="col-md-6 col-lg-4">
        <div class="login-wrap p-0">
            {#if errorMsg}
                <AlertBox message={errorMsg}/>
            {/if}
            <form on:submit|preventDefault={login}  class="signin-form">
                <div class="form-group">
                    <input type="username" class="form-control" placeholder="Username" required bind:value={username}>
                </div>
                <div class="form-group">
                    <input id="password-field" type="password" class="form-control" placeholder="Password" required bind:value={password}>
                    <span toggle="#password-field" class="fa fa-fw fa-eye field-icon toggle-password"></span>
                </div>
                <div class="form-group">
                    <button type="submit" class="form-control btn btn-primary submit px-3">Sign In</button>
                </div>
                <small> To log in as a guest use (username:guest, password: guest) <small>

            </form>
        </div>
    </div>
</div>
</div>

<!-- <style>
    .form-container {
      height: 200px;
      position: relative;
      border: 3px solid green;
    }
    
    .center {
      margin: 0;
      position: absolute;
      top: 50%;
      left: 50%;
      -ms-transform: translate(-50%, -50%);
      transform: translate(-50%, -50%);
    }
</style> -->