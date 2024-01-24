from rest_framework import serializers
from employer.models import Employer



class EmployerSerializer(serializers.ModelSerializer):
    """
    main model serializer class of the Employer model.
    this needed to represent the values as json
    """
    class Meta:
        model = Employer
        fields = ["first_name","last_name","email","phone"]


class GetProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(default="no email provided")


    def get_profile(self,cleaned_data):
        try:
            specific_employer = Employer.objects.get(email=cleaned_data["email"])
            employer = EmployerSerializer(specific_employer)
            employer_data = employer.data
            return True,employer_data
        
        except:
            error_message = {"error":"user not found"}
            return False,error_message
        

class UpdateProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(default="no email provided")
    required_field = serializers.DictField()

    def update_profile(self,cleaned_data):
        unchangable_fields = ["id","user_id","email","created_at","job_position_id","department","groups","user","permission","permissions","admin","task","lead"]
        try:
            specific_employer = Employer.objects.get(email=cleaned_data["email"])
            
            for key,values in cleaned_data["required_field"].items():
                if key in unchangable_fields:
                    return False,{"permission error":"you cant change this fields"}
                
                setattr(specific_employer,key,values)
            specific_employer.save()

            employer_serialized = EmployerSerializer(specific_employer)

            return True,employer_serialized.data

        except:
            error_message = {"error":"user not found"}
            return False,error_message
        
