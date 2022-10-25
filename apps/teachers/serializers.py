from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        if 'student' in attrs:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')
        if attrs['teacher'].id != self.instance.teacher.id:
            raise serializers.ValidationError('Teacher cannot grade for other teacher''s assignment')
        if 'content' in attrs:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')
        if self.instance.state == 'GRADED':
            raise serializers.ValidationError('GRADED assignments cannot be graded again')
        if self.instance.state == 'DRAFT':
            raise serializers.ValidationError('SUBMITTED assignments can only be graded')

        if self.partial:
            return attrs

        return super().validate(attrs)
