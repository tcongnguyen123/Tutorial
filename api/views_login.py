from .library import *
class View_Login_Set(ViewSet):
    def register(self,request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            if username and password:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                return Response({'message':'Register success'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'Register failed'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'Register failed'},status=status.HTTP_400_BAD_REQUEST)
