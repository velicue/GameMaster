Everything is string not Integer!
#Users

api/user/register 
request: {'email': $email, 'pwd': $pwd} 
response: {'success' = true} or {'success' = false} 

---

api/user/login 
request: {'email': $email, 'pwd': $pwd} 
response: {'success' = true} or {'success' = false} 

---

api/user/repeat 
request: {'email': $email} 
response: {'repeat' = true} or {'repeat' = false} 

