"use client"

import { useEffect, useRef } from "react"
import type { StickFigureCanvasProps } from "./types" // Assuming StickFigureCanvasProps is declared in a separate file
import { connections, keypointMap } from "./constants" // Assuming connections and keypointMap are declared in a separate file

export function StickFigureCanvas({ poses, width, height }: StickFigureCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const scaleX = width / 640 // Assuming 640 is the original width for scaling
  const scaleY = height / 480 // Assuming 480 is the original height for scaling

  useEffect(() => {
    if (!canvasRef.current || !poses.length) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, width, height)

    const gradient = ctx.createLinearGradient(0, 0, 0, height)
    gradient.addColorStop(0, "#1a1a2e")
    gradient.addColorStop(1, "#16213e")
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, width, height)

    // Draw poses
    poses.forEach((pose) => {
      drawStickFigure(ctx, pose.keypoints, width, height)
    })
  }, [poses, width, height])

  const drawStickFigure = (
    ctx: CanvasRenderingContext2D,
    keypoints: any[],
    canvasWidth: number,
    canvasHeight: number,
  ) => {
    ctx.shadowColor = "#00ff88"
    ctx.shadowBlur = 5
    ctx.strokeStyle = "#00ff88"
    ctx.lineWidth = 4
    ctx.lineCap = "round"
    ctx.lineJoin = "round"

    connections.forEach(([start, end]) => {
      const startPoint = keypointMap.get(start)
      const endPoint = keypointMap.get(end)

      if (startPoint && endPoint && startPoint.confidence > 0.5 && endPoint.confidence > 0.5) {
        const connectionGradient = ctx.createLinearGradient(startPoint.x, startPoint.y, endPoint.x, endPoint.y)
        connectionGradient.addColorStop(0, "#00ff88")
        connectionGradient.addColorStop(1, "#00ccff")
        ctx.strokeStyle = connectionGradient

        ctx.beginPath()
        ctx.moveTo(startPoint.x * scaleX, startPoint.y * scaleY)
        ctx.lineTo(endPoint.x * scaleX, endPoint.y * scaleY)
        ctx.stroke()
      }
    })

    // Reset shadow for joints
    ctx.shadowBlur = 0

    keypoints.forEach((kp) => {
      if (kp.confidence > 0.5) {
        const x = kp.x * scaleX
        const y = kp.y * scaleY

        // Joint circle with confidence-based size
        const jointSize = 3 + kp.confidence * 3
        ctx.fillStyle = "#ff6b6b"
        ctx.beginPath()
        ctx.arc(x, y, jointSize, 0, 2 * Math.PI)
        ctx.fill()

        // Confidence ring
        ctx.strokeStyle = `rgba(255, 255, 255, ${kp.confidence * 0.8})`
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(x, y, jointSize + 2, 0, 2 * Math.PI)
        ctx.stroke()
      }
    })
  }

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        className="border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-900"
      />
      <div className="absolute top-2 left-2 text-xs text-white bg-black bg-opacity-50 px-2 py-1 rounded">
        Live Stick Figure Mimicking
      </div>
    </div>
  )
}
