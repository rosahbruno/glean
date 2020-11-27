initSidebarItems({"enum":[["Lifetime","The supported metrics' lifetimes."]],"fn":[["global_glean","Gets a reference to the global Glean object."],["initialize","Creates and initializes a new Glean object."],["register_ping_type","Register a new `PingType`."],["set_experiment_active","Indicate that an experiment is running.  Glean will then add an experiment annotation to the environment which is sent with pings. This infomration is not persisted between runs."],["set_experiment_inactive","Indicate that an experiment is no longer running."],["set_upload_enabled","Sets whether upload is enabled or not."],["setup_glean","Sets or replaces the global Glean object."],["shutdown","Shuts down Glean."],["submit_ping","Collects and submits a ping for eventual uploading."],["submit_ping_by_name","Collects and submits a ping for eventual uploading by name."],["test_reset_glean","TEST ONLY FUNCTION. Resets the Glean state and triggers init again."]],"mod":[["net","Handling the Glean upload logic."],["private","The different metric types supported by the Glean SDK to handle data."]],"struct":[["ClientInfoMetrics","Metrics included in every ping as `client_info`."],["CommonMetricData","The common set of data shared across all different metric types."],["Configuration","The Glean configuration."],["Error","A specialized `Error` type for this crate's operations."],["Glean","The object holding meta information about a Glean instance."]],"type":[["Result","A specialized `Result` type for this crate's operations."]]});