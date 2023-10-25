build-PutItemFunction:
	mvn clean package
	mvn dependency:copy-dependencies -DexcludeScope=provided
	cp -rf ./target/classes/* $(ARTIFACTS_DIR)/