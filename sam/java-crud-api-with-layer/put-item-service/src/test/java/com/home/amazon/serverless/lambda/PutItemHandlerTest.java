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
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class PutItemHandlerTest {

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
    public void shouldPutItemIfBodyIsValid() {
        Book testBook = new Book();
        testBook.setIsbn(TEST_PARTITION_KEY_VALUE);
        when(client.table(eq(TEST_TABLE_NAME), any(TableSchema.class))).thenReturn(table);
        when(request.getBody()).thenReturn(new Gson().toJson(testBook));

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            PutItemHandler handler = new PutItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            verify(table).putItem(eq(testBook));
            assertEquals(PutItemHandler.STATUS_CODE_CREATED, response.getStatusCode());
        }

    }

    @Test
    public void shouldNotPutItemIfBodyIsNotValid() {
        when(request.getBody()).thenReturn(StringUtils.EMPTY);

        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            PutItemHandler handler = new PutItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            verifyNoInteractions(table);
            assertEquals(PutItemHandler.STATUS_CODE_NO_CONTENT, response.getStatusCode());
        }
    }

    @Test
    public void shouldNotPutItemIfBodyIsMissed() {
        try (MockedStatic<DependencyFactory> dependencyFactoryMockedStatic = mockStatic(DependencyFactory.class)) {
            dependencyFactoryMockedStatic.when(DependencyFactory::dynamoDbEnhancedClient).thenReturn(client);
            dependencyFactoryMockedStatic.when(DependencyFactory::tableName).thenReturn(TEST_TABLE_NAME);
            PutItemHandler handler = new PutItemHandler();
            APIGatewayProxyResponseEvent response = handler.handleRequest(request, context);
            verifyNoInteractions(table);
            assertEquals(PutItemHandler.STATUS_CODE_NO_CONTENT, response.getStatusCode());
        }
    }

}