from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Please choose an image no larger than 2MB.'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Please choose an image with width less than 4096px.'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Please choose an image with height less than 4096px.'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = ['id', 'owner', 'is_owner', 'profile_id', 'profile_image',
                  'created_at', 'updated_at', 'title', 'content',
                  'image', 'image_filter', 'like_id', ]