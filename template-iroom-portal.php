<?php
/*
Template Name: 이룸덴탈랩 포털
Description: 기공소 관리 시스템 전용 페이지
*/

// 워드프레스 헤더 제거
?>
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>이룸덴탈랩 포털</title>
<style>
body {margin: 0 !important;padding: 0 !important;overflow: hidden;}
#iframe-container {position: fixed;top: 0;left: 0;width: 100%;height: 100vh;border: none;overflow: hidden;}
#iframe-container iframe {width: 100%;height: 100%;border: none;}
.error-box {position: fixed;top: 50%;left: 50%;transform: translate(-50%, -50%);background: #fff3cd;border: 3px solid #ffc107;padding: 30px;border-radius: 10px;max-width: 700px;font-family: Arial, sans-serif;box-shadow: 0 4px 20px rgba(0,0,0,0.2);}
.error-box h2 {color: #856404;margin-top: 0;}
.error-box code {background: #f5f5f5;padding: 3px 8px;border-radius: 4px;font-size: 13px;display: inline-block;margin: 5px 0;}
.error-box .path-list {background: #f8f9fa;padding: 15px;border-radius: 5px;margin: 15px 0;max-height: 300px;overflow-y: auto;}
.error-box .success {color: #28a745;font-weight: bold;}
.error-box .fail {color: #dc3545;}
</style>
</head>
<body>

<?php
// 여러 가능한 경로 시도
$possible_paths = array(
    // 1. 테마 폴더 내부 (가장 일반적)
    array(
        'url' => get_template_directory_uri() . '/iroom-portal/iroom-portal-preview_1.html',
        'path' => get_template_directory() . '/iroom-portal/iroom-portal-preview_1.html',
        'description' => '테마 폴더 내부'
    ),
    // 2. 자식 테마 폴더
    array(
        'url' => get_stylesheet_directory_uri() . '/iroom-portal/iroom-portal-preview_1.html',
        'path' => get_stylesheet_directory() . '/iroom-portal/iroom-portal-preview_1.html',
        'description' => '자식 테마 폴더'
    ),
    // 3. uploads 폴더
    array(
        'url' => content_url() . '/iroom-portal/iroom-portal-preview_1.html',
        'path' => WP_CONTENT_DIR . '/iroom-portal/iroom-portal-preview_1.html',
        'description' => 'wp-content 폴더'
    ),
    // 4. 루트/opencode 폴더 (현재 위치)
    array(
        'url' => home_url('/opencode/iroom-portal-preview_1.html'),
        'path' => ABSPATH . 'opencode/iroom-portal-preview_1.html',
        'description' => '루트/opencode 폴더'
    ),
);

$found_path = null;
$checked_paths = array();

// 각 경로 확인
foreach ($possible_paths as $option) {
    $exists = file_exists($option['path']);
    $checked_paths[] = array(
        'description' => $option['description'],
        'url' => $option['url'],
        'path' => $option['path'],
        'exists' => $exists
    );
    
    if ($exists && empty($found_path)) {
        $found_path = $option['url'];
    }
}

// 파일을 찾았으면 iframe 표시
if ($found_path) {
    ?>
    <div id="iframe-container">
      <iframe src="<?php echo esc_url($found_path); ?>" 
              frameborder="0" 
              allowfullscreen>
      </iframe>
    </div>
    <?php
} else {
    // 에러 메시지
    ?>
    <div class="error-box">
        <h2>⚠️ HTML 파일을 찾을 수 없습니다</h2>
        
        <p><strong>찾는 파일:</strong> <code>iroom-portal-preview_1.html</code></p>
        
        <div style="background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">📁 올바른 파일 위치</h3>
            <p>다음 중 <strong>한 곳</strong>에 파일을 업로드하세요:</p>
            
            <p><strong>방법 1 (권장):</strong><br>
            <code><?php echo get_template_directory(); ?>/iroom-portal/iroom-portal-preview_1.html</code></p>
            
            <p><strong>방법 2:</strong><br>
            <code><?php echo ABSPATH; ?>opencode/iroom-portal-preview_1.html</code><br>
            <small>(현재 파일 위치)</small></p>
        </div>
        
        <h3>🔍 확인한 경로들:</h3>
        <div class="path-list">
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #e9ecef;">
                    <th style="padding: 8px; text-align: left;">위치</th>
                    <th style="padding: 8px; text-align: left;">경로</th>
                    <th style="padding: 8px; text-align: center; width: 80px;">상태</th>
                </tr>
                <?php foreach ($checked_paths as $check) : ?>
                <tr style="border-bottom: 1px solid #dee2e6;">
                    <td style="padding: 8px;"><strong><?php echo esc_html($check['description']); ?></strong></td>
                    <td style="padding: 8px;"><code style="font-size: 11px;"><?php echo esc_html($check['path']); ?></code></td>
                    <td style="padding: 8px; text-align: center;">
                        <?php if ($check['exists']) : ?>
                            <span class="success">✅ 있음</span>
                        <?php else : ?>
                            <span class="fail">❌ 없음</span>
                        <?php endif; ?>
                    </td>
                </tr>
                <?php endforeach; ?>
            </table>
        </div>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107;">
            <h3 style="margin-top: 0;">💡 빠른 해결 방법</h3>
            <ol style="margin: 10px 0; padding-left: 20px;">
                <li>FTP 프로그램으로 접속</li>
                <li><strong>테마 폴더</strong>로 이동:<br>
                    <code><?php echo get_template_directory(); ?></code></li>
                <li><code>iroom-portal</code> 폴더 생성 (없으면)</li>
                <li><code>iroom-portal-preview_1.html</code> 파일 업로드</li>
                <li>이 페이지 새로고침</li>
            </ol>
        </div>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h3 style="margin-top: 0;">ℹ️ 현재 워드프레스 정보</h3>
            <ul style="list-style: none; padding: 0;">
                <li><strong>테마 이름:</strong> <?php echo wp_get_theme()->get('Name'); ?></li>
                <li><strong>테마 버전:</strong> <?php echo wp_get_theme()->get('Version'); ?></li>
                <li><strong>테마 경로:</strong><br><code><?php echo get_template_directory(); ?></code></li>
                <li><strong>사이트 URL:</strong> <code><?php echo home_url(); ?></code></li>
            </ul>
        </div>
        
        <p style="margin-top: 20px; text-align: center; font-size: 14px; color: #6c757d;">
            파일을 업로드한 후 이 페이지를 <strong>새로고침</strong>하세요.
        </p>
    </div>
    <?php
}
?>

<?php wp_footer(); ?>
</body>
</html>
