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
import software.amazon.awssdk.enhanced.dynamodb.TableSchema;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class UpdateItemHandlerTest {

    private static final String TEST_TABLE_NAME = "TestTable";
    private static final String TEST_PARTITION_KEY_VALUE = "123";
    private static final String TEST_AUTHOR_NAME = "TestAuthor";

    @Mock
    private DynamoDbEnhancedClient client;

    @Mock
    private DynamoDbTable<Book> table;

    @Mock
    private APIGatewayProxyRequestEvent request;

    @Mock
    private Context context;

    @Test
    public void shouldUpdateItemIfBodyIsValid() {
        Book testBook = new Book();
        testBook.setIsbn(TEST_PARTITION_KEY_VALUE);
        testBook.setName(TEST_AUTHOR_NAME);
        when(client.table(eq(TEST_TABLE_NAME), any(TableSchema.class))).thenReturn(table);
        Gson gson = new Gson();
        when(request.getBody()).thenReturn(gson.toJson(testBook));
        when(table.updateItem(eq(testBook))).thenReturn(testBook);

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            UpdateItemHandler handler = new UpdateItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            verify(table).updateItem(eq(testBook));
            assertEquals(testBook, gson.fromJson(response.getBody(), Book.class));
        }

    }

    @Test
    public void shouldNotUpdateItemIfBodyMissed() {

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            UpdateItemHandler handler = new UpdateItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            verifyNoInteractions(table);
            assertTrue(StringUtils.isEmpty(response.getBody()));
        }

    }

}