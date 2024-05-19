class otp_verification_view(APIView):
    def post(self,request):
        try:
            data=request.data
            otp=data.get('otp')
            if not otp:
                return Response({"error": "OTP is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            user_details=request.session.get('user_details') 
            if not user_details:
                return Response({"error": "User details not found."}, status=status.HTTP_400_BAD_REQUEST)  
            
    