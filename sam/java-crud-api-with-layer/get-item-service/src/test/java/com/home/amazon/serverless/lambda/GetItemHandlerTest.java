package com.home.amazon.serverless.lambda;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import com.home.amazon.serverless.core.Book;
import com.home.amazon.serverless.core.DependencyFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.Key;
import software.amazon.awssdk.enhanced.dynamodb.TableSchema;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class GetItemHandlerTest {

    private static final String TEST_TABLE_NAME = "TestTable";
    private static final String TEST_PARTITION_KEY_VALUE = "123";


    @Mock
    private DynamoDbEnhancedClient client;

    @Mock
    private DynamoDbTable<Book> table;

    @Mock
    private APIGatewayProxyRequestEvent request;

    @Mock
    private Context context;

    @BeforeEach
    public void setUp() {
        when(client.table(eq(TEST_TABLE_NAME), any(TableSchema.class))).thenReturn(table);
    }

    @Test
    public void shouldReturnItemIfExists() {
        Map<String, String> pathParameters = new HashMap<>();
        pathParameters.put(Book.PARTITION_KEY, TEST_PARTITION_KEY_VALUE);
        Book testBook = new Book();
        testBook.setIsbn(TEST_PARTITION_KEY_VALUE);
        when(table.getItem(any(Key.class))).thenReturn(testBook);
        when(request.getPathParameters()).thenReturn(pathParameters);

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            GetItemHandler handler = new GetItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            assertEquals(200, response.getStatusCode());
            assertTrue(response.getBody().contains(TEST_PARTITION_KEY_VALUE));
        }
    }

    @Test
    public void shouldReturnEmptyResponseIfItemNotExists() {
        when(table.getItem(any(Key.class))).thenReturn(null);
        when(request.getPathParameters()).thenReturn(new HashMap<>());

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            GetItemHandler handler = new GetItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            assertEquals(200, response.getStatusCode());
            assertTrue(response.getBody().isEmpty());
        }

    }

    @Test
    public void shouldReturnEmptyResponseIfPathParameterMissed() {
        when(request.getPathParameters()).thenReturn(null);

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            GetItemHandler handler = new GetItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            assertEquals(200, response.getStatusCode());
            assertTrue(response.getBody().isEmpty());
        }
    }

}