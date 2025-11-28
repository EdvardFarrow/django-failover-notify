from rest_framework import serializers
from .models import Notification, default_channels



VALID_CHANNELS = {'email', 'sms', 'telegram'}



class NotificationSerializer(serializers.ModelSerializer):
    channels_chain = serializers.ListField(
        child=serializers.CharField(), 
        required=False, 
        default=default_channels
    )
    
    class Meta:
        model = Notification
        fields = ['recipient', 'message', 'channels_order']
        
    def validate_channels_chain(self, value):
        for channel in value:
            if channel not in VALID_CHANNELS:
                raise serializers.ValidationError(f"Unknown channel: {channel}")
        return value