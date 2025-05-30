from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Value, IntegerField, Case, When
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.exceptions import ValidationError
from .models import Candidate
from .serializers import CandidateSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '').strip()
        
        if not search:
            return queryset

        # Input validation
        if len(search) > 100:  
            raise ValidationError("Search term too long")

        try:
            search_words = search.split()
            if not search_words:
                return queryset

            # Build OR conditions for each word
            conditions = Q()
            for word in search_words:
                #NOTE below cond is optional just for performance
                if len(word) >= 2:  # Only search for words with 2 or more characters
                    conditions |= Q(name__icontains=word)
            
            # Get all matching candidates
            queryset = queryset.filter(conditions)
            
            # Order by exact matches first, then partial matches 
            exact_match = ' '.join(search_words)
            queryset = queryset.annotate(
                exact_match=Case(
                    When(name__iexact=exact_match, then=Value(2)),
                    When(name__icontains=exact_match, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ).order_by('-exact_match', 'name')

            return queryset

        except Exception as e:
            # TODO - add logger for prod 
            print(f"Search error: {str(e)}")  # Temporary debug print
            return Candidate.objects.none()

    @action(detail=False, methods=['get'])
    def search(self, request):
        try:
            queryset = self.get_queryset()
            
            # Debug print
            print(f"Search term: {request.query_params.get('search', '')}")
           
            
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                response = self.get_paginated_response(serializer.data)
                # Add search metadata
                response.data['search_metadata'] = {
                    'total_results': self.paginator.page.paginator.count,
                    'search_term': request.query_params.get('search', ''),
                    'page': self.paginator.page.number,
                    'total_pages': self.paginator.page.paginator.num_pages,
                }
                return response
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Error in search view: {str(e)}")  # Temporary debug print
            return Response(
                {'error': 'An error occurred while processing your request'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
