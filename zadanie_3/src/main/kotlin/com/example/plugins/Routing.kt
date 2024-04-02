package com.example.plugins

import io.ktor.server.application.*
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.http.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.plugins.contentnegotiation.*
//import io.ktor.client.engine.curl.*


fun Application.configureRouting() {
    routing {
        get("/") {

            val webhookUrl =
                "https://discord.com/api/webhooks/1223592495473229864/51pnHpQdRZvr-xpFXvv6vwjJTrvVCH76D_-_KUnhwrYX9pbytm2o1Rb13MsPo-neirPw"
            val message = "dsagdasgdagdasgdsag!"

            val client = HttpClient(CIO) {
                //install(ContentType("application/json"))
            }

            val command = listOf(
                "curl", "-X", "POST", webhookUrl,
                "-H", "Content-Type: application/json",
                "-d", "{\"content\": \"$message\"}"
            )

            val process = ProcessBuilder(command)
                .redirectErrorStream(true)
                .start()

            process.waitFor()

            // Odczytujemy wynik działania procesu
            val responseCode = process.exitValue()

            val payload = mapOf(
                "content" to message
            )

            try {
                client.post(webhookUrl) {
                    contentType(ContentType.Application.Json)
                    setBody("{\"content\": \"$message\"}")
                }
                call.respondText("Message sent to Discord!")
            } catch (e: Exception) {
                call.respondText("Error sending message to Discord: ${e.message}")
            } finally {
                client.close()
            }
        }
    }
}
