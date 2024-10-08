/*
 * Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 */
package io.airbyte.cdk.integrations

import io.airbyte.cdk.integrations.base.Integration
import io.airbyte.cdk.integrations.base.adaptive.AdaptiveSourceRunner
import io.airbyte.commons.features.EnvVariableFeatureFlags
import io.airbyte.commons.features.FeatureFlags
import io.airbyte.commons.json.Jsons
import io.airbyte.commons.resources.MoreResources
import io.airbyte.protocol.models.v0.ConnectorSpecification

abstract class BaseConnector : Integration {
    open val featureFlags: FeatureFlags = EnvVariableFeatureFlags()

    val isCloudDeployment
        get() =
            AdaptiveSourceRunner.CLOUD_MODE.equals(featureFlags.deploymentMode(), ignoreCase = true)
    /**
     * By convention the spec is stored as a resource for java connectors. That resource is called
     * spec.json.
     *
     * @return specification.
     * @throws Exception
     * - any exception.
     */
    @Throws(Exception::class)
    override fun spec(): ConnectorSpecification {
        // return a JsonSchema representation of the spec for the integration.
        val resourceString = MoreResources.readResource("spec.json")
        return Jsons.deserialize(resourceString, ConnectorSpecification::class.java)
    }
}
