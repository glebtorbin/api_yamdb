from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title_id, author=user).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить больше одного отзыва!'
                )
        return data

    def validate_score(self, value):
        if 1 > value > 10:
            raise serializers.ValidationError(
                'Оценка может быть от 1 до 10'
            )
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'pub_date', 'author', 'score')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'pub_date', 'author', 'review')
