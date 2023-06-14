# from rest_framework.views import exception_handler
# from rest_framework import generics, status

# class CustomException(Exception):
#     _default_code = 400

#     def __init__(
#         self,
#         message: str = "",
#         status_code=status.HTTP_400_BAD_REQUEST,
#         data=None,
#         code: int = _default_code,
#     ):

#         self.code = code
#         self.status = status_code
#         self.message = message
#         if data is None:
#             self.data = {"detail": message}
#         else:
#             self.data = data

#     def __str__(self):
#         return self.message

# class ExecuteError(CustomException):
#     "" "execution error" ""
#     default_code = 500
#     default_message = "execution error"


# # class UnKnowError(CustomException):
# #     "" "execution error" ""
# #     default_code = 500
# #     default_ Message = "unknown error"


# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
    
#     #Here, the customized customexception is returned directly to ensure that other exceptions in the system will not be affected
#     if isinstance(exc, CustomException):
#         return Response(data=exc.data, status=exc.status)
#     response = exception_handler(exc, context)
#     return response