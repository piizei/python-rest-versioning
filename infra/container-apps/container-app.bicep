param location string = resourceGroup().location

resource containerApp 'Microsoft.App/containerApps@2022-03-01' = {
  name: 'python-testing-app'
  location: location
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      secrets: [
        {
          name: 'container-registry-password'
          value: containerRegistry.listCredentials().passwords[0].value
        }
      ]      
      registries: [
        {
          server: containerRegistry.name
          username: containerRegistry.properties.loginServer
          passwordSecretRef: 'container-registry-password'
        }
      ]
      ingress: {
        external: true
        targetPort: 5000
      }
    }
    template: {
      containers: [
        {
          // Use dummy container on first provisioning, as the ACR is not yet ready.
          image: 'nginx'
          name: 'dummy'
        }
      ]
      scale: {
        minReplicas: 0
      }
    }
  }
}

@minLength(5)
@maxLength(50)
@description('Provide a globally unique name of your Azure Container Registry')
param acrName string = 'acr${uniqueString(resourceGroup().id)}'

@description('Provide a tier of your Azure Container Registry.')
param acrSku string = 'Basic'

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-06-01-preview' = {
  name: acrName
  location: location
  sku: {
    name: acrSku
  }
  properties: {
    adminUserEnabled: true
  }
}


output fqdn string = containerApp.properties.configuration.ingress.fqdn


resource env 'Microsoft.App/managedEnvironments@2022-03-01' = {
  name: 'python-testing-app-env'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: law.properties.customerId
        sharedKey: listKeys(law.id,law.apiVersion).primarySharedKey
      }
    }
  }
}
output id string = env.id

resource law 'Microsoft.OperationalInsights/workspaces@2020-03-01-preview' = {
  name: 'python-testing-app-log-analytics'
  location: location
  properties: any({
    retentionInDays: 30
    features: {
      searchVersion: 1
    }
    sku: {
      name: 'PerGB2018'
    }
    workspaceCapping: {
      dailyQuotaGb: 1
    }
  })
}
