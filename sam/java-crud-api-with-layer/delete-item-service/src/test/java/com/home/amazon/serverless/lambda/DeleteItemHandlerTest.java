package com.home.amazon.serverless.lambda;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import com.google.gson.Gson;
import com.home.amazon.serverless.core.Book;
import com.home.amazon.serverless.core.DependencyFactory;
import org.apache.commons.lang3.StringUtils;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.Key;
import software.amazon.awssdk.enhanced.dynamodb.TableSchema;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class DeleteItemHandlerTest {

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

    @Test
    public void shouldDeleteAndReturnItem() {
        Book testBook = new Book();
        testBook.setIsbn(TEST_PARTITION_KEY_VALUE);
        when(client.table(eq(TEST_TABLE_NAME), any(TableSchema.class))).thenReturn(table);
        Map<String, String> pathParameters = new HashMap<>();
        pathParameters.put(Book.PARTITION_KEY, TEST_PARTITION_KEY_VALUE);
        when(request.getPathParameters()).thenReturn(pathParameters);
        when(table.deleteItem(eq(Key.builder().partitionValue(TEST_PARTITION_KEY_VALUE).build()))).thenReturn(testBook);

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            DeleteItemHandler handler = new DeleteItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            verify(table).deleteItem(eq(Key.builder().partitionValue(TEST_PARTITION_KEY_VALUE).build()));
            assertEquals(testBook, new Gson().fromJson(response.getBody(), Book.class));
        }
    }

    @Test
    public void shouldNotTouchTableIfKeyMissed() {
        when(client.table(eq(TEST_TABLE_NAME), any(TableSchema.class))).thenReturn(table);
        when(request.getPathParameters()).thenReturn(Collections.emptyMap());

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            DeleteItemHandler handler = new DeleteItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            verifyNoInteractions(table);
            assertTrue(StringUtils.isEmpty(response.getBody()));
        }

    }

    @Test
    public void shouldNotTouchTableIfPathParametersAbsent() {
        when(client.table(eq(TEST_TABLE_NAME), any(TableSchema.class))).thenReturn(table);

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            DeleteItemHandler handler = new DeleteItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            verifyNoInteractions(table);
            assertTrue(StringUtils.isEmpty(response.getBody()));
        }

    }


}