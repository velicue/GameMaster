Everything is string not Integer!
#Users

api/user/register para: {'email': $email, 'pwd': $pwd} return: {'success' = '1'} or {'success' = '0'} 

api/user/login para: {'email': $email, 'pwd': $pwd} return: {'success' = '1'} or {'success' = '0'} 

api/user/repeat para: {'email': $email} return: {'repeat' = '1'} or {'repeat' = '0'} // repeat = 1 means the email is repeated

